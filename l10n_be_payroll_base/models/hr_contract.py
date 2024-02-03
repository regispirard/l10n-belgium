# Copyright 2023 TINCID (Régis Pirard)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrContract(models.Model):

    _name = "hr.contract"
    _inherit = ["hr.contract", "hr.onss.be.mixin"]

    bik_be = fields.Float(string="Benefit in kind (other)")
