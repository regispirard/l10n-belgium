# Copyright 2024 TINCID SRL, Régis Pirard
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import UserError


class HrPayslip(models.Model):
    _name = "hr.payslip"
    _inherit = ["hr.payslip", "hr.onss.be.mixin"]

    @api.onchange("employee_id", "date_from", "date_to")
    def onchange_employee(self):
        res = super(HrPayslip, self).onchange_employee()
        for payslip in self:
            if payslip.state == "done" or payslip.contract_id.country_code != "BE":
                continue
            if not payslip.contract_id.onssbe_type:
                raise UserError(_("Security social position not defined on contract"))

            if payslip.contract_id:
                payslip.onssbe_type = payslip.contract_id.onssbe_type

        return res
