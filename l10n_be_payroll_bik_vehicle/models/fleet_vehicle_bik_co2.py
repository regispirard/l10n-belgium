# Copyright 2023 TINCID SRL, Régis Pirard
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class FleetVehicleBikCo2(models.Model):

    _name = "fleet.vehicle.bik.co2"
    _description = "CO2 reference to compute vehicle benefit in kind"

    year = fields.Integer()
    fiscal_fuel_type = fields.Selection(
        selection=[
            ("diesel", "Diesel"),
            ("gasoline", "Gasoline"),
        ],
        string="Fuel Type",
        required=True,
    )
    ref_co2 = fields.Integer(
        string="Reference CO2",
        required=True,
    )

    @api.model
    def _get_fiscal_fuel_type(self, vehicle_fuel_type):
        match vehicle_fuel_type:
            case "diesel" | "plug_in_hybrid_diesel":
                return "diesel"
            case "gasoline" | "plug_in_hybrid_gasoline" | "full_hybrid" | "lpg" | "cng":
                return "gasoline"
            case _:
                return "electric"

    @api.model
    def _get_co2_reference_history(self, fiscal_fuel_type):
        return self.search([("fiscal_fuel_type", "=", fiscal_fuel_type)])

    def _get_co2_rate(self, vehicle_co2):
        # Return CO2 rate for a give vehicle
        co2_rate = 0.055 + ((vehicle_co2 - self.ref_co2) * 0.001)
        if co2_rate > 0.18:
            co2_rate = 0.18
        if co2_rate < 0.04:
            co2_rate = 0.04
        return co2_rate

    @api.model
    def _get_co2_rate_fuel_year(self, fiscal_fuel_type, vehicle_co2, year):
        if fiscal_fuel_type == "electric":
            co2_rate = 0.04
        else:
            ref_history = self._get_co2_reference_history(fiscal_fuel_type)
            # check if year is configured
            ref_years = ref_history.mapped("year")
            if year not in ref_years:
                if year < min(ref_years):
                    year = min(ref_years)
                else:
                    year = max(ref_years)
            # get ref_co2
            ref_co2 = ref_history.filtered_domain([("year", "=", year)])
            # get rate
            co2_rate = ref_co2._get_co2_rate(vehicle_co2)
        return co2_rate
