# Copyright 2023 TINCID SRL, Régis Pirard
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class FleetBikMin(models.Model):

    _name = "fleet.bik.min"
    _description = (
        "Benefit in kind - Minimal value of benefit in kind for each fiscal period."
    )

    _sql_constraints = [
        (
            "year_unique",
            "unique(year)",
            "You can only define the minimal amount for a year once.",
        ),
    ]

    year = fields.Integer(required=True, string="Fiscal Period")
    amount = fields.Float(
        required=True,
    )
