# Copyright 2023 TINCID SRL, Régis Pirard
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrEmployeePrivate(models.Model):

    _inherit = "hr.employee"

    tax_be_type = fields.Selection(
        [
            ("leader", "Enterprise leader"),
            ("employee", "Employee"),
        ],
        groups="hr.group_hr_user",
        tracking=True,
        default="employee",
    )
    tax_be_children_valid = fields.Integer(
        string="Number of Dependent Children (valid)",
        groups="hr.group_hr_user",
        tracking=True,
    )
    tax_be_children_invalid = fields.Integer(
        string="Number of Dependent Children (invalid)",
        groups="hr.group_hr_user",
        tracking=True,
        help="""Belgique :
            Par "enfant handicapé", il faut entendre :
            - l'enfant atteint à 66 p.c. au moins d'une insuffisance ou diminution de
            capacité physique ou psychique du chef d'une ou de plusieurs affections ;
            - l'enfant dont il est établi, indépendamment de son âge, qu'en raison de
            faits survenus et constatés avant l'âge de 65 ans :
                a) soit son état physique ou psychique a réduit sa capacité de gain à
                un tiers ou moins de ce qu'une personne valide est en mesure de gagner
                en exerçant une profession sur le marché général du travail ;
                b) soit son état de santé provoque un manque total d'autonomie ou une
                réduction d'autonomie d'au moins 9 points, mesurés conformément aux
                guide et échelle médico-sociale applicables dans le cadre de la
                législation relative aux allocations aux handicapés ;
                c) soit, après la période d'incapacité primaire prévue à l'article 87
                de la loi coordonnée relative à l'assurance obligatoire soins de
                santé et indemnités, sa capacité de gain est réduite à un tiers
                ou moins comme prévu à l'article 100 de la même loi coordonnée ;
                d) soit, par une décision administrative ou judiciaire, qu'il est
                handicapé physiquement ou psychiquement ou en incapacité de travail
                de façon permanente pour au moins 66 p.c.""",
    )
    tax_be_other_dependent = fields.Integer(
        string="Number of Dependent Persons", groups="hr.group_hr_user", tracking=True
    )
