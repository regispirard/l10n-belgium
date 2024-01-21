# Copyright 2023 TINCID SRL, Régis Pirard
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date, datetime

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    bik_be_ids = fields.One2many(
        comodel_name="fleet.vehicle.bik",
        inverse_name="vehicle_id",
        string="Benefit in kid",
        compute="_compute_bik_ids",
        readonly=True,
        store=True,
    )
    is_bik_be_computed = fields.Boolean(
        string="Vehicle BIK computed",
        compute="_compute_bik_ids",
        store=True,
    )

    def _get_degressive_ranges(self):
        ranges = [
            # (before age in month, devaluation percentage)
            # None = over 60 month
            (12, 1),
            (24, 0.94),
            (36, 0.88),
            (48, 0.82),
            (60, 0.76),
            (None, 0.70),
        ]
        return ranges

    def _get_degressive_periods(self, vehicle):
        ranges = vehicle._get_degressive_ranges()
        periods = []
        start_date = datetime(
            vehicle.acquisition_date.year, vehicle.acquisition_date.month, 1
        )
        range_start_date = start_date

        for age, percentage in ranges:
            if age is not None:
                range_end_date = (
                    start_date + relativedelta(months=age) - relativedelta(days=1)
                )
            else:
                range_end_date = False
            periods.append(
                (
                    range_start_date,
                    range_end_date,
                    percentage,
                )
            )

            if range_end_date:
                range_start_date = range_end_date + relativedelta(days=1)
        return periods

    def _get_co2_reference_electric(self):
        # electric: no co2 reference
        co2_reference = {
            # (year, reference co2)
            2012: 0,
            2013: 0,
            2014: 0,
            2015: 0,
            2016: 0,
            2017: 0,
            2018: 0,
            2019: 0,
            2020: 0,
            2021: 0,
            2022: 0,
            2023: 0,
        }
        return co2_reference

    def _get_co2_reference_diesel(self):
        # diesel
        co2_reference = {
            # (year, reference co2)
            2012: 95,
            2013: 95,
            2014: 93,
            2015: 91,
            2016: 89,
            2017: 87,
            2018: 86,
            2019: 88,
            2020: 91,
            2021: 84,
            2022: 75,
            2023: 67,
        }
        return co2_reference

    def _get_co2_reference_other(self):
        # other fuel types
        co2_reference = {
            # (year, reference co2)
            2012: 115,
            2013: 116,
            2014: 112,
            2015: 110,
            2016: 107,
            2017: 105,
            2018: 105,
            2019: 107,
            2020: 111,
            2021: 102,
            2022: 91,
            2023: 82,
        }
        return co2_reference

    def _get_co2_reference(self, fuel_type):
        if fuel_type == "electric":
            co2_reference = self._get_co2_reference_electric()
            return co2_reference
        if fuel_type == "diesel":
            co2_reference = self._get_co2_reference_diesel()
            return co2_reference
        # other fuel types
        co2_reference = self._get_co2_reference_other()
        return co2_reference

    def _get_co2_ref_from_year(self, year, co2_reference):
        if year in co2_reference:
            co2_ref = co2_reference[year]
        else:
            min_year = min(co2_reference.keys())
            max_year = max(co2_reference.keys())
            if year < min_year:
                co2_ref = co2_reference[min_year]
            else:
                co2_ref = co2_reference[max_year]
        return co2_ref

    def _get_degressive_co2_periods(self, degressive_periods, co2_reference):
        periods = []
        for deg_start_date, deg_end_date, deg_percentage in degressive_periods:
            if not deg_start_date:
                deg_start_date = deg_end_date - relativedelta(year=1)
            if not deg_end_date:
                deg_end_date = deg_start_date + relativedelta(year=1)
            i = deg_end_date.year - deg_start_date.year
            yn = deg_start_date.year
            while i > 0:
                # Year n
                co2_ref_n = self._get_co2_ref_from_year(yn, co2_reference)
                periods.append(
                    (
                        date(yn, deg_start_date.month, deg_start_date.day),
                        date(yn, 12, 31),
                        deg_percentage,
                        co2_ref_n,
                    ),
                )
                # Year n+1
                yn1 = yn + 1
                co2_ref_n1 = self._get_co2_ref_from_year(yn1, co2_reference)
                periods.append(
                    (
                        date(yn1, 1, 1),
                        date(yn1, deg_end_date.month, deg_end_date.day),
                        deg_percentage,
                        co2_ref_n1,
                    ),
                )
                i = i - 1
                yn = yn + 1
        co2_ref_n = self._get_co2_ref_from_year(yn, co2_reference)
        periods.append(
            (
                date(yn, deg_start_date.month, deg_start_date.day),
                False,
                deg_percentage,
                co2_ref_n,
            ),
        )
        return periods

    def _compute_co2_rate_from_co2_ref(self, co2_ref, co2_vehicle):
        co2_rate = 0.055 + ((co2_vehicle - co2_ref) * 0.001)
        if co2_rate > 0.18:
            co2_rate = 0.18
        if co2_rate < 0.04:
            co2_rate = 0.04
        return co2_rate

    @api.depends(
        "acquisition_date",
        "country_id",
        "car_value",
        "co2",
        "fuel_type",
        "country_code",
    )
    def _compute_bik_ids(self):
        for vehicle in self:
            if (
                not vehicle.car_value
                or not vehicle.acquisition_date
                or not vehicle.co2
                or not vehicle.fuel_type
                or vehicle.country_code != "BE"
            ):
                # Will remove all previous computations
                vehicle.bik_be_ids = [(5, 0)]
                vehicle.is_bik_be_computed = False
                return

            # Remove all previous computations
            bik_items = [(5, 0)]  # Will unlink all records

            # BIK will decrease in time - we get the periods
            degressive_periods = vehicle._get_degressive_periods(vehicle)

            # CO2 rate change every year and depends on fuel_type - get periods
            co2_reference = vehicle._get_co2_reference(vehicle.fuel_type)

            # Mix degressive and co2 periods
            periods = vehicle._get_degressive_co2_periods(
                degressive_periods, co2_reference
            )

            # Compute BIK for each period
            for start_date, end_date, percentage, co2_ref in periods:

                co2_rate = vehicle._compute_co2_rate_from_co2_ref(co2_ref, vehicle.co2)

                amount = vehicle.car_value * percentage * (6 / 7) * co2_rate

                bik_data = {
                    "vehicle_id": vehicle.id,
                    "date_from": start_date,
                    "date_to": end_date,
                    "amount": amount,
                }

                bik_items.append((0, 0, bik_data))

            vehicle.bik_be_ids = bik_items
            vehicle.is_bik_be_computed = True
        return
