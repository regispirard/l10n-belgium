# Copyright 2023 TINCID SRL, Régis Pirard
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class FleetVehicleBikBe(models.Model):

    _name = "fleet.vehicle.bik"
    _description = "Benefit in kind for the vehicle"

    vehicle_id = fields.Many2one(
        comodel_name="fleet.vehicle",
        string="Vehicle",
        readonly=True,
        required=True,
        ondelete="cascade",
    )
    date_from = fields.Date(
        string="From",
        readonly=True,
    )
    date_to = fields.Date(
        string="To",
        readonly=True,
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        related="vehicle_id.currency_id",
        readonly=True,
    )
    amount = fields.Monetary(
        default=0.0,
        required=True,
        readonly=True,
    )
