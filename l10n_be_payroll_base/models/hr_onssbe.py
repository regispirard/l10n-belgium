# Copyright 2023 TINCID SRL, Régis Pirard
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrOnssBeMixin(models.AbstractModel):

    _name = "hr.onss.be.mixin"
    _description = "Fields Belgian Social Security"

    onssbe_type = fields.Selection(
        [
            ("leader", "Enterprise leader"),
            ("employee", "Employee"),
            ("none", "Non soumis"),
        ],
        string="Social Security Position (BE)",
    )
