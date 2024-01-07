# Copyright 2023 TINCID SRL, Régis Pirard
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import math

from odoo import fields, models


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    marital_status_be = fields.Selection(
        [
            ("single", "Single"),
            ("married", "Married"),
            ("cohabitant", "Legal Cohabitant"),
            ("widower", "Widower"),
            ("divorced", "Divorced"),
        ],
        string="Marital Status",
        tracking=True,
    )

    tax_be_type = fields.Selection(
        [
            ("leader", "Enterprise leader"),
            ("employee", "Employee"),
        ],
        groups="hr.group_hr_user",
        tracking=True,
    )

    def _compute_marital_status_be(self):
        if self.employee_id.marital and self.status != "done":
            self.marital_status = self.employee_id.marital

    def compute_sheet(self):
        # get data from employee
        self._compute_marital_status()
        return super().compute_sheet()

    def _round_amount_be(self, amount) -> float:
        # Belgian rounding rule
        # Round the amount up or down to the nearest cent depending
        # on whether or not the thousandths digit reaches 5.
        nbDecimals = len(str(amount).split(".")[1])
        if nbDecimals <= 3:
            amount_trunc = amount
        else:
            stepper = 10.0**3
            amount_trunc = math.trunc(stepper * amount) / stepper
        amount_integer = int(amount_trunc * 1000)
        amount_thousands = amount_integer % 10
        if amount_thousands >= 5:
            # Round to superior cent
            rounded_amount = (amount_integer // 10 + 1) / 100
        else:
            # Round to inferior cent
            rounded_amount = amount_integer // 10 / 100
        return rounded_amount

    def _compute_gross_annual_revenue_leader(self):
        gross_annual_revenue_leader = "TODO"
        return gross_annual_revenue_leader

    def _compute_gross_annual_revenue_employee(self):
        gross_annual_revenue_employee = "TODO"
        return gross_annual_revenue_employee

    def _compute_gross_annual_revenue(self):
        gross_annual_revenue = "TODO"
        return gross_annual_revenue

    def _compute_income_tax_be(
        self,
        revenue,
    ):

        if self.marital == "single":
            return revenue * 1000
        if self.marital == "married":
            return revenue / 10
        return revenue
