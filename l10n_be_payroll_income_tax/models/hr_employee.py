# Copyright 2023 TINCID SRL, Régis Pirard
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class HrEmployeePrivate(models.Model):

    _name = "hr.employee"
    _inherit = ["hr.employee", "hr.tax.be.mixin"]
