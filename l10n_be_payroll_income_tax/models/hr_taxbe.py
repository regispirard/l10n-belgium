# Copyright 2023 TINCID SRL, Régis Pirard, Fabio Lucarelli
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import datetime
import math

from odoo import api, fields, models


class HrTaxContractBeMixin(models.AbstractModel):

    _name = "hr.tax.contract.be.mixin"
    _description = "Fields to compute Belgian income taxes (contract)"

    taxbe_type = fields.Selection(
        [
            ("leader", "Enterprise leader"),
            ("employee", "Employee"),
            ("none", "Non soumis"),
        ],
        string="Fiscal position (BE)",
    )


class HrTaxBeMixin(models.AbstractModel):

    _name = "hr.tax.be.mixin"
    _description = "Fields to compute Belgian income taxes (employee)"

    taxbe_children = fields.Integer(
        string="Dependent Children",
        groups="hr.group_hr_user",
        help="""L'enfant handicapé à charge est compté pour deux.
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

    taxbe_children_hand = fields.Integer(
        string="Dependent Childrens (With Handicap)",
        groups="hr.group_hr_user",
        help="""L'enfant handicapé à charge est compté pour deux.
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

    taxbe_isolated = fields.Boolean(
        string="Isolated",
        help="""le bénéficiaire des revenus est un isolé,
        SAUF lorsque ses revenus se
        composent de PENSIONS ou d’ALLOCATIONS DE CHOMAGE AVEC
        COMPLEMENT D’ENTREPRISE (visées à l’article 146, CIR 92)
        """,
    )

    taxbe_isolated_par = fields.Boolean(
        string="Isolated Parent",
        help="""Le bénéficiaire des revenus est un veuf (une veuve)
        non remarié(e), un père (une mère) célibataire, ou un parent
        divorcé ou séparé de fait, avec un ou plusieurs enfants à charge
        """,
    )

    taxbe_handicap = fields.Boolean(
        string="Handicap",
        help="""Le bénéficiaire des revenus est lui-même handicapé
        """,
    )

    taxbe_dependant_65 = fields.Integer(
        string="65+ Dependant Persons",
        help="""Le bénéficiaire des revenus a à sa charge des personnes
        visées à l'article 136, 2° et 3°, CIR 92 qui sont dans une situation
        de dépendance et qui ont atteint l’âge de 65 ans (par personne).
        Est considérée comme étant en situation de dépendance la personne
        pour laquelle le degré d'autonomie est évalué à au moins 9 points
        conformément à l'arrêté ministériel du 30 juillet 1987 fixant les
        catégories et le guide pour l'évaluation du degré d'autonomie en vue
        de l'examen du droit à l'allocation d'intégration. La situation de
        dépendance est constatée par la Direction générale Personnes
        handicapées du SPF Sécurité sociale, Medex ou le médecin-conseil
        auprès de la mutualité, ou une institution ou personne similaire
        d'un autre Etat membre de l'Espace économique européen.""",
    )

    taxbe_person_65 = fields.Integer(
        string="65+ Persons",
        help="""le bénéficiaire des revenus a à sa charge des personnes
        visées à l'article 136, 2° et 3°, CIR 92 qui ont atteint l’âge de
        65 ans (par personne).
        Concerne une mesure transitoire jusqu'à l'année des revenus 2024,
        prévue à l'article 546, CIR 92.
        La personne handicapée à charge est comptée pour deux.""",
    )

    taxbe_person_other = fields.Integer(
        string="Other Persons (-65)",
        help="""Le bénéficiaire des revenus a à sa charge des personnes
        visées à l'article 136, 2° à 4°, CIR 92 autres que celles visées
        aux points 4 et 5 ci-avant (par personne).
        La personne handicapée à charge est comptée pour deux.""",
    )

    taxbe_spouse_without_rev = fields.Boolean(
        string="Spouse Without Revenues",
    )

    taxbe_spouse_low_rev = fields.Boolean(
        string="Spouse With Low Revenues (<263)",
        help="""Le conjoint du bénéficiaire des revenus a des revenus
        professionnels propres, autres que des pensions, rentes ou revenus
        y assimilés, qui ne dépassent pas 263,00 EUR NETS par mois.
        Pour apprécier la limites de 263,00 EUR NETS par mois, il y a lieu
        d'envisager la situation au 1er janvier et de déterminer les revenus
        professionnels nets comme suit :
            1. diminuer les revenus professionnels bruts des retenues ou des
            cotisations obligatoires applicables en exécution de la législation
            sociale ou d'un statut légal ou réglementaire y assimilé ;
            2. diminuer ensuite la différence obtenue de 20 p.c.""",
    )

    taxbe_spouse_low_pens = fields.Boolean(
        string="Spouse With Low Pension (<525)",
        help="""le conjoint du bénéficiaire des revenus a des revenus
        professionnels propres qui sont exclusivement constitués de pensions,
        rentes ou revenus y assimilés, qui ne dépassent pas 525,00 EUR NETS
        par mois.
        Pour apprécier la limites de 525,00 EUR NETS par mois, il y a lieu
        d'envisager la situation au 1er janvier et de déterminer les revenus
        professionnels nets comme suit :
            1. diminuer les revenus professionnels bruts des retenues ou des
            cotisations obligatoires applicables en exécution de la législation
            sociale ou d'un statut légal ou réglementaire y assimilé ;
            2. diminuer ensuite la différence obtenue de 20 p.c.""",
    )

    @api.model
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

    @api.model
    def _get_soc_plaf1(self, year):
        match year:
            case "2022":
                return 1210.00
            case "2023":
                return 1260.00
            case "2024":
                return 1260.00
            case _:
                return 1260.00

    @api.model
    def _get_soc_amount1(self, year):
        match year:
            case "2022":
                return 335.00
            case "2023":
                return 345.00
            case "2024":
                return 345.00
            case _:
                return 345.00

    @api.model
    def _get_soc_plaf2(self, year):
        match year:
            case "2022":
                return 5210.00
            case "2023":
                return 5440.00
            case "2024":
                return 5440.00
            case _:
                return 5440.00

    @api.model
    def _get_soc_perc2(self, year):
        return 0.2150

    @api.model
    def _get_soc_plaf3(self, year):
        match year:
            case "2022":
                return 7670.00
            case "2023":
                return 8015.00
            case "2024":
                return 8015.00
            case _:
                return 8015.00

    @api.model
    def _get_soc_perc3(self, year):
        return 0.1450

    @api.model
    def get_estimated_social_security_leader(self, year, amount):
        reduction = 0.00

        plaf1 = self._get_soc_plaf1(year)
        amount1 = self._get_soc_amount1(year)

        plaf2 = self._get_soc_plaf2(year)
        perc2 = self._get_soc_perc2(year)

        plaf3 = self._get_soc_plaf3(year)
        perc3 = self._get_soc_perc3(year)

        if amount <= plaf1:
            reduction = amount1
        elif (plaf1 + 0.01) <= amount <= plaf2:
            stage1 = amount1
            reduction = stage1 + (perc2 * (amount - plaf1))
        elif (plaf2 + 0.01) <= amount <= plaf3:
            stage1 = amount1
            stage2 = stage1 + (perc2 * (plaf2 - plaf1))
            reduction = stage1 + stage2 + (perc3 * (plaf3 - plaf2))
        else:
            stage1 = amount1
            stage2 = stage1 + (perc2 * (plaf2 - plaf1))
            stage3 = stage1 + stage2 + (perc3 * (plaf3 - plaf2))
            reduction = stage1 + stage2 + stage3

        reduction = self._round_amount_be(reduction)
        return reduction

    @api.model
    def _get_annexe1_year(self, year):
        match year:
            case "2023":
                return [
                    [15170, 0, 0.2675, 0.2675 * 15170],
                    [24260, 15170, 0.4280, 0.4280 * (24260 - 15170)],
                    [46340, 24260, 0.4815, 0.4815 * (46340 - 24260)],
                    [999999, 46340, 0.5350, 0],
                ]
            case "2024":
                return [
                    [15170, 0, 0.2675, 0.2675 * 15170],
                    [24260, 15170, 0.4280, 0.4280 * (24260 - 15170)],
                    [46340, 24260, 0.4815, 0.4815 * (46340 - 24260)],
                    [999999, 46340, 0.5350, 0],
                ]
            case _:
                return [
                    [15170, 0, 0.2675, 0.2675 * 15170],
                    [24260, 15170, 0.4280, 0.4280 * (24260 - 15170)],
                    [46340, 24260, 0.4815, 0.4815 * (46340 - 24260)],
                    [999999, 46340, 0.5350, 0],
                ]

    @api.model
    def _get_annexe3_year(self, year):
        match year:
            case "2023":
                return [0, 540, 1476, 3912, 6804, 9972, 13128, 16308, 19824]
            case "2024":
                return [0, 540, 1476, 3912, 6804, 9972, 13128, 16308, 19824]
            case _:
                return [0, 540, 1476, 3912, 6804, 9972, 13128, 16308, 19824]

    @api.model
    def _get_annexe3_sup_year(self, year):
        match year:
            case "2023":
                return 3516.00
            case "2024":
                return 3516.00
            case _:
                return 3516.00

    @api.model
    def _get_annexe4_year(self, year):
        match year:
            case "2023":
                return [
                    144,  # 0 Isolé
                    540,  # 1 Veuf - Pere/Mere celibataire
                    540,  # 2 Handicapé
                    1728,  # 3 A Charge > 65 ans dépendant
                    1140,  # 4 A Charge > 65 ans
                    540,  # 5 A Charge autre
                    1578,  # 6 Conjoint à charge sans rev < plafond (263 net/mois)
                    3150,  # 7 Conjoint à charge avec rev < plafond (525 net/mois)
                ]
            case "2024":
                return [
                    144,  # 0 Isolé
                    540,  # 1 Veuf - Pere/Mere celibataire
                    540,  # 2 Handicapé
                    1728,  # 3 A Charge > 65 ans dépendant
                    1140,  # 4 A Charge > 65 ans
                    540,  # 5 A Charge autre
                    1578,  # 6 Conjoint à charge sans rev < plafond (263 net/mois)
                    3150,  # 7 Conjoint à charge avec rev < plafond (525 net/mois)
                ]
            case _:
                return [
                    144,  # 0 Isolé
                    540,  # 1 Veuf - Pere/Mere celibataire
                    540,  # 2 Handicapé
                    1728,  # 3 A Charge > 65 ans dépendant
                    1140,  # 4 A Charge > 65 ans
                    540,  # 5 A Charge autre
                    1578,  # 6 Conjoint à charge sans rev < plafond (263 net/mois)
                    3150,  # 7 Conjoint à charge avec rev < plafond (525 net/mois)
                ]

    @api.model
    def _get_exempt_quotity_year(self, year):
        match year:
            case "2023":
                return 9620.00
            case "2024":
                return 9620.00
            case _:
                return 9620.00

    @api.model
    def _get_pct_lump_sum(self, year, taxbe_type):
        if taxbe_type == "employee":
            match year:
                case "2023":
                    return 0.3
                case "2024":
                    return 0.3
                case _:
                    return 0.3
        if taxbe_type == "leader":
            match year:
                case "2023":
                    return 0.03
                case "2024":
                    return 0.03
                case _:
                    return 0.03

    @api.model
    def _get_max_lump_sum(self, year, taxbe_type):
        if taxbe_type == "employee":
            match year:
                case "2023":
                    return 5510.00
                case "2024":
                    return 5510.00
                case _:
                    return 5510.00
        if taxbe_type == "leader":
            match year:
                case "2023":
                    return 2910.00
                case "2024":
                    return 2910.00
                case _:
                    return 2910.00

    @api.model
    def _get_max_max_spouse_rev(self, year):
        match year:
            case "2023":
                return 12520.00
            case "2024":
                return 12520.00
            case _:
                return 12520.00

    @api.model
    def _get_income_tax_base(
        self,
        taxable,
        year=datetime.date.today().year,
        taxbe_type="employee",
        spouse_without_revenue=False,
    ):

        # get parameters for the year
        annexe1 = self._get_annexe1_year(year)
        exempt_quotity = self._get_exempt_quotity_year(year)
        pct_lump_sum = self._get_pct_lump_sum(year, taxbe_type)
        max_lump_sum = self._get_max_lump_sum(year, taxbe_type)
        max_spouse_rev = self._get_max_max_spouse_rev(year)

        # Gross annual revenues
        if taxbe_type == "leader":
            estimated_soc_sec = self.get_estimated_social_security_leader(year, taxable)
            gross_rev = self._round_amount_be(taxable - estimated_soc_sec)
        else:
            gross_rev = self._round_amount_be(taxable)
        gross_annual_rev = gross_rev * 12

        # Lump-sum expenses
        lump_sum_exp = min(round(gross_annual_rev * pct_lump_sum, 2), max_lump_sum)

        # Net annual revenues
        net_annual_rev = gross_annual_rev - lump_sum_exp

        if spouse_without_revenue:
            spouse_revenue = round(
                min(net_annual_rev * pct_lump_sum, max_spouse_rev), 2
            )
            net_annual_rev -= spouse_revenue
        else:
            spouse_revenue = 0

        # Compute base income tax

        income_tax_base = 0
        income_tax_spouse = 0

        for x in annexe1:
            if net_annual_rev > x[0]:
                income_tax_base += x[3]
            else:
                income_tax_base += (net_annual_rev - x[1]) * x[2]
                break

        for x in annexe1:
            if spouse_revenue > x[0]:
                income_tax_spouse += x[3]
            else:
                income_tax_spouse += (spouse_revenue - x[1]) * x[2]
                break

        income_tax_base = max(
            0.00,
            income_tax_base
            + income_tax_spouse
            - round(
                exempt_quotity * annexe1[0][2] * (2 if (spouse_without_revenue) else 1),
                2,
            ),
        )

        income_tax_base = self._round_amount_be(income_tax_base)

        return income_tax_base

    @api.model
    def _get_income_tax_reductions(
        self,
        year,
        childrens=0,
        childrens_hand=0,
        isolated=False,
        isolated_par=False,
        handicap=False,
        dependant_65=0,
        person_65=0,
        person_other=0,
        spouse_low_rev=False,
        spouse_low_pens=False,
    ):
        reduction = 0.00

        # get parameters for the year
        annexe3 = self._get_annexe3_year(year)
        annexe3_sup = self._get_annexe3_sup_year(year)
        annexe4 = self._get_annexe4_year(year)

        # Children
        if childrens < 9:
            reduction += annexe3[childrens]
        else:
            reduction += annexe3[8] + annexe3_sup * (childrens - 8)

        # Children with handicap
        if childrens_hand < 9:
            reduction += annexe3[(childrens_hand * 2)]
        else:
            reduction += annexe3[8] + annexe3_sup * ((childrens_hand * 2) - 8)

        # Isolated
        if isolated:
            reduction += annexe4[0]

        # Isolated Parent
        if isolated_par:
            reduction += annexe4[1]

        # Handicap
        if handicap:
            reduction += annexe4[2]

        # 65+ dependant people
        if dependant_65 > 0:
            reduction += annexe4[3] * dependant_65

        # 65+ dependant people
        if person_65 > 0:
            reduction += annexe4[4] * person_65

        # other people
        if person_other > 0:
            reduction += annexe4[5] * person_other

        # Spouse with low revenue
        if spouse_low_rev:
            reduction += annexe4[6]

        # Spouse with rent < thresold
        if spouse_low_pens:
            reduction += annexe4[7]

        income_tax_reductions = self._round_amount_be(reduction)
        return income_tax_reductions

    @api.model
    def get_income_tax(
        self,
        taxable,
        year=datetime.date.today().year,
        taxbe_type="employee",
        spouse_without_revenue=False,
        childrens=0,
        childrens_hand=0,
        isolated=False,
        isolated_par=False,
        handicap=False,
        dependant_65=0,
        person_65=0,
        person_other=0,
        spouse_low_rev=False,
        spouse_low_pens=False,
    ):

        # Compute base income tax
        income_tax_base = self._get_income_tax_base(
            taxable, year, taxbe_type, spouse_without_revenue
        )

        # Compute reductions
        income_tax_reduction = self._get_income_tax_reductions(
            year,
            childrens,
            childrens_hand,
            isolated,
            isolated_par,
            handicap,
            dependant_65,
            person_65,
            person_other,
            spouse_low_rev,
            spouse_low_pens,
        )

        # Compute income tax

        income_tax = (income_tax_base - income_tax_reduction) / 12
        income_tax = self._round_amount_be(income_tax)

        # Income tax should be positive
        if income_tax < 0:
            income_tax = 0.00

        return income_tax
