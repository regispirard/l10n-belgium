# Copyright 2023 TINCID (Régis Pirard)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "OCA Payroll localisation Belgium - Base module",
    "author": "TINCID (Régis PIRARD), Odoo Community Association (OCA)",
    "summary": "Manage payroll in Belgium with OCA Payroll app (Base module)",
    "website": "https://github.com/OCA/l10n-belgium",
    "category": "Localization",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "hr_contract",
        "payroll",
        "payroll_structure_template",
    ],
    "data": [
        "data/hr_payroll_structure.xml",
        "views/hr_contract.xml",
    ],
    "application": True,
}
