# Copyright 2023 TINCID SRL, Régis Pirard
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class HrPayslip(models.Model):

    _name = "hr.payslip"
    _inherit = [
        "hr.payslip",
        "hr.tax.be.mixin",
        "hr.tax.contract.be.mixin",
    ]

    @api.onchange("employee_id", "date_from", "date_to")
    def onchange_employee(self):
        res = super(HrPayslip, self).onchange_employee()
        for payslip in self:
            if payslip.state == "done":
                continue
            if payslip.contract_id:
                payslip.taxbe_type = payslip.contract_id.taxbe_type
            if payslip.employee_id.marital:
                # TO DO
                continue
        return res
