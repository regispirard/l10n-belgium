# Copyright 2023 TINCID SRL, Régis Pirard
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class FleetVehicleBikCo2(models.Model):

    _name = "fleet.vehicle.bik.co2"
    _description = "CO2 reference to compute vehicle benefit in kind"

    year = fields.Integer()
    fiscal_fuel_type = fields.Selection(
        selection=[
            ("diesel", "Diesel"),
            ("gasoline", "Gasoline"),
            ("electric", "Electric"),
        ],
        string="Fuel Type",
        required=True,
    )
    ref_co2 = fields.Integer(
        string="Reference CO2",
        required=True,
    )
