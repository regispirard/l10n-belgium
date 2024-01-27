# Copyright 2023 TINCID SRL, Régis Pirard
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "OCA Payroll localisation Belgium - Benefit in kind vehicle",
    "author": "TINCID (Régis PIRARD), Odoo Community Association (OCA)",
    "summary": "Manage payroll in Belgium : Benefits in kind - vehicles",
    "website": "https://github.com/OCA/l10n-belgium",
    "category": "Localization",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "hr",
        "hr_fleet",
        "payroll",
        "payroll_account",
        "l10n_be_payroll_base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/fleet_vehicle.xml",
        "views/fleet_bik_co2.xml",
        "views/fleet_bik_degressive.xml",
        "views/fleet_bik_min.xml",
        "views/menuitem.xml",
        "data/hr_payroll_structure.xml",
        "data/fleet_bik_co2.xml",
        "data/fleet_bik_degressive.xml",
        "data/fleet_bik_min.xml",
    ],
    "application": True,
}
