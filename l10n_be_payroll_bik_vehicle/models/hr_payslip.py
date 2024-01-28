# Copyright 2024 TINCID SRL, Régis Pirard
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    bik_car_ids = fields.One2many(
        comodel_name="hr.payslip.car",
        inverse_name="payslip_id",
        string="Company Cars",
    )

    @api.onchange("employee_id", "date_from", "date_to")
    def onchange_employee(self):
        super(HrPayslip, self).onchange_employee()
        for payslip in self:
            car_assignations = self.env["fleet.vehicle.assignation.log"].search(
                [
                    ("driver_employee_id", "!=", False),
                    ("driver_employee_id", "=", payslip.employee_id.id),
                    "|",
                    ("date_start", "<=", payslip.date_to),
                    ("date_start", "=", False),
                    "|",
                    ("date_end", ">=", payslip.date_from),
                    ("date_end", "=", False),
                ]
            )

            bik_car_ids = [(5, 0)]

            for car in car_assignations:
                # Compute assignation start date for this payroll month
                start_date = payslip.date_from
                if car.date_start:
                    if car.date_start > start_date:
                        start_date = car.date_start
                # Compute assignation end date for this payroll month
                end_date = payslip.date_to
                if car.date_end:
                    if car.date_end < end_date:
                        end_date = car.date_end

                bik_car = {
                    "payslip_id": payslip.id,
                    "car_id": car.vehicle_id.id,
                    "period_from": start_date,
                    "period_to": end_date,
                }

                bik_car_ids.append((0, 0, bik_car))

        payslip.bik_car_ids = bik_car_ids
        return
