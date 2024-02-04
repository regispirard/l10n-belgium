# Copyright 2023 TINCID SRL, Régis Pirard
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "OCA Payroll localisation Belgium - Income Tax",
    "author": "TINCID (Régis PIRARD), Odoo Community Association (OCA)",
    "summary": "Manage payroll in Belgium : Income Tax",
    "website": "https://github.com/OCA/l10n-belgium",
    "category": "Localization",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "hr",
        "payroll",
        "payroll_details",
        "l10n_be_payroll_base",
    ],
    "data": [
        "views/hr_payslip.xml",
        "views/hr_contract.xml",
        "data/hr_payroll_structure.xml",
    ],
    "application": False,
}
