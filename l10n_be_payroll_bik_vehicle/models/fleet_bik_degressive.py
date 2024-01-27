# Copyright 2023 TINCID SRL, Régis Pirard
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class FleetBikDegressive(models.Model):

    _name = "fleet.bik.degressive"
    _description = """Benefit in kind - Degressive percentage to apply at
    each anniversary date of the vehicle."""

    _sql_constraints = [
        (
            "month_min_max",
            "month_max > month_min",
            "Month to should be greater than month from ",
        ),
    ]

    month_from = fields.Integer(
        required=True,
    )
    month_to = fields.Integer()
    degressive_percentage = fields.Float(
        required=True,
    )
