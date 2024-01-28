# Copyright 2024 TINCID SRL, Régis Pirard
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import calendar

from odoo import api, fields, models


class HrPayslipCar(models.Model):
    _name = "hr.payslip.car"
    _description = "Company cars to be taken into account when computing the payslip"

    payslip_id = fields.Many2one(
        string="Payslip",
        comodel_name="hr.payslip",
        required=True,
    )
    car_id = fields.Many2one(
        string="Car",
        comodel_name="fleet.vehicle",
        required=True,
    )
    period_from = fields.Date(
        string="From",
        required=True,
    )
    period_to = fields.Date(
        string="To",
        required=True,
    )
    period_days = fields.Integer(
        string="Days",
        compute="_compute_bik",
        store=True,
    )
    bik_yearly = fields.Float(
        string="Base BIK Amount",
        compute="_compute_bik",
        store=True,
    )
    bik_amount = fields.Float(
        string="BIK Amount",
        compute="_compute_bik",
        store=True,
    )

    @api.depends(
        "car_id",
        "period_from",
        "period_to",
    )
    def _compute_bik(self):
        for car in self:
            if not car.car_id or not car.period_from or not car.period_to:
                return
            days_year = 366 if calendar.isleap(car.period_from.year) else 365

            car.period_days = (car.period_to - car.period_from).days + 1

            bik_yearly_car = car.car_id.bik_be_ids.filtered_domain(
                [("date_from", "<=", car.period_to), ("date_to", ">=", car.period_from)]
            )
            if len(bik_yearly_car) != 1:
                car.bik_amount = 0
                return

            car.bik_yearly = bik_yearly_car.amount

            car.bik_amount = (car.bik_yearly / days_year) * car.period_days
