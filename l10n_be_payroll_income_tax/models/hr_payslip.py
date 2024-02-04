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
            if payslip.employee_id:
                payslip.taxbe_children = payslip.employee_id.taxbe_children
                payslip.taxbe_children_hand = payslip.employee_id.taxbe_children_hand
                payslip.taxbe_isolated = payslip.employee_id.taxbe_isolated
                payslip.taxbe_isolated_par = payslip.employee_id.taxbe_isolated_par
                payslip.taxbe_handicap = payslip.employee_id.taxbe_handicap
                payslip.taxbe_dependant_65 = payslip.employee_id.taxbe_dependant_65
                payslip.taxbe_person_65 = payslip.employee_id.taxbe_person_65
                payslip.taxbe_person_other = payslip.employee_id.taxbe_person_other
                payslip.taxbe_spouse_without_rev = (
                    payslip.employee_id.taxbe_spouse_without_rev
                )
                payslip.taxbe_spouse_low_rev = payslip.employee_id.taxbe_spouse_low_rev
                payslip.taxbe_spouse_low_pens = (
                    payslip.employee_id.taxbe_spouse_low_pens
                )
        return res
