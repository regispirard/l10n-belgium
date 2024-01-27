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
        degressive_model = self.env["fleet.bik.degressive"]
        ranges = degressive_model.search([])
        return ranges

    def _get_degressive_periods(self, vehicle):
        # Compute degressive periods based on vehicle acquisition date
        # BIK decreases at each vehicle anniversary
        d_ranges = vehicle._get_degressive_ranges()
        periods = []
        start_date = datetime(
            vehicle.acquisition_date.year, vehicle.acquisition_date.month, 1
        )

        for d_range in d_ranges:
            range_start_date = start_date + relativedelta(months=d_range.month_from - 1)
            if d_range.month_to:
                range_end_date = (
                    start_date
                    + relativedelta(months=d_range.month_to)
                    - relativedelta(days=1)
                )
            else:
                range_end_date = False
            periods.append(
                (
                    range_start_date,
                    range_end_date,
                    d_range.degressive_percentage,
                )
            )

        return periods

    def _get_degressive_co2_periods(
        self, degressive_periods, fiscal_fuel_type, vehicle_co2
    ):
        co2_model = self.env["fleet.bik.co2"]
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
                co2_rate_n = co2_model._get_co2_rate_fuel_year(
                    fiscal_fuel_type, vehicle_co2, yn
                )
                periods.append(
                    (
                        date(yn, deg_start_date.month, deg_start_date.day),
                        date(yn, 12, 31),
                        deg_percentage,
                        co2_rate_n,
                    ),
                )
                # Year n+1
                yn1 = yn + 1
                co2_rate_n1 = co2_model._get_co2_rate_fuel_year(
                    fiscal_fuel_type, vehicle_co2, yn1
                )
                periods.append(
                    (
                        date(yn1, 1, 1),
                        date(yn1, deg_end_date.month, deg_end_date.day),
                        deg_percentage,
                        co2_rate_n1,
                    ),
                )
                i = i - 1
                yn = yn + 1
        co2_rate_n = co2_model._get_co2_rate_fuel_year(
            fiscal_fuel_type, vehicle_co2, yn
        )
        periods.append(
            (
                date(yn, deg_start_date.month, deg_start_date.day),
                False,
                deg_percentage,
                co2_rate_n,
            ),
        )
        return periods

    def _get_bik_min_year(self):
        min_list = {}
        for bkm in self.env["fleet.bik.min"].search([]):
            min_list[bkm.year] = bkm.amount
        return min_list

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

            co2_model = self.env["fleet.bik.co2"]

            # Remove all previous computations
            bik_items = [(5, 0)]  # Will unlink all records

            # BIK will decrease in time - we get the periods
            degressive_periods = vehicle._get_degressive_periods(vehicle)

            # Get fiscal fuel type
            fiscal_fuel_type = co2_model._get_fiscal_fuel_type(vehicle.fuel_type)

            # Get CO2 reference table for this fuel type
            # co2_ref_table = co2_model._get_co2_reference_history(fiscal_fuel_type)

            # Get all periods and CO2 data for fuel type
            periods_data = vehicle._get_degressive_co2_periods(
                degressive_periods, fiscal_fuel_type, vehicle.co2
            )

            # Get minimal BIK amount per year
            bik_min_year = vehicle._get_bik_min_year()

            # Compute BIK for each period
            for start_date, end_date, percentage, co2_rate in periods_data:

                amount = vehicle.car_value * percentage * (6 / 7) * co2_rate

                # Apply minimal BIK amount
                min_amount = bik_min_year.get(start_date.year)
                if min_amount:
                    if amount < min_amount:
                        amount = min_amount

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
