# Copyright 2023 TINCID (Régis Pirard)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrContract(models.Model):

    _inherit = "hr.contract"

    bik_be = fields.Float(string="Benefit in kind (other)")
