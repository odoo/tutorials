from odoo import api, fields, models


class HrContract(models.Model):
    _inherit = 'hr.contract'

    l10n_in_basic_salary = fields.Monetary(string="Basic Salary", help="Basic salary calculated from the wage", compute="_compute_l10n_in_basic_salary", inverse="_inverse_l10n_in_basic_salary", currency_field="currency_id")
    l10n_in_house_rent_allowance = fields.Monetary(string="House Rent Allowance", compute="_compute_l10n_in_house_rent_allowance", inverse="_inverse_l10n_in_house_rent_allowance", currency_field="currency_id")
    l10n_in_standard_allowance = fields.Monetary(string="Standard Allowance", default=lambda self: self.env.company.l10n_in_standard_allowance, currency_field="currency_id")
    l10n_in_performance_bonus = fields.Monetary(string="Performance Bonus", compute="_compute_l10n_in_performance_bonus", inverse="_inverse_l10n_in_performance_bonus", currency_field="currency_id")
    l10n_in_leave_travel_allowance = fields.Monetary(string="Leave Travel Allowance", compute="_compute_l10n_in_leave_travel_allowance", inverse="_inverse_l10n_in_leave_travel_allowance", currency_field="currency_id")
    l10n_in_leave_allowance = fields.Monetary(string="Leave Allowance", compute="_compute_leave_allowance", inverse="_inverse_leave_allowance", currency_field="currency_id")
    l10n_in_leave_days = fields.Float(string="Leave Days", default=lambda self: self.env.company.l10n_in_leave_days)
    l10n_in_gratuity = fields.Monetary(string="Gratuity", currency_field="currency_id", default=lambda self: self.env.company.l10n_in_gratuity)
    l10n_in_supplementary_allowance = fields.Monetary(string="Supplementary Allowance", compute="_compute_l10n_in_supplementary_allowance", inverse="_inverse_l10n_in_supplementary_allowance", currency_field="currency_id", default=lambda self: self.env.company.l10n_in_supplementary_allowance)

    l10n_in_basic_salary_percent = fields.Float(string="Basic Salary Percentage", help="basic salary percentage of wage", default=lambda self: self.env.company.l10n_in_basic_salary_percent)
    l10n_in_house_rent_allowance_percent = fields.Float(string="House Rent Allowance Percentage", help="this is the percentage of basic salary", default=lambda self: self.env.company.l10n_in_house_rent_allowance_percent)
    l10n_in_standard_allowance_percent = fields.Float(string="Standard Allowance Percentage", compute="_compute_l10n_in_standard_allowance_percent", inverse="_inverse_l10n_in_standard_allowance_percent")
    l10n_in_performance_bonus_percent = fields.Float(string="Performance Bonus Percentage", default=lambda self: self.env.company.l10n_in_performance_bonus_percent)
    l10n_in_leave_travel_allowance_percent = fields.Float(string="Leave Travel Allowance Percentage", default=lambda self: self.env.company.l10n_in_leave_travel_allowance_percent)
    l10n_in_leave_allowance_per_day_percent = fields.Float(string="Leave allowance per day percentage")
    l10n_in_leave_allowance_percent = fields.Float(string="Leave Allowance Percentage")
    l10n_in_gratuity_percent = fields.Float(string="Gratuity Percentage", compute="_compute_l10n_in_gratuity_percent", inverse="_inverse_l10n_in_gratuity_percent")
    l10n_in_supplementary_allowance_percent = fields.Float(string="Supplementary Allowance Percentage")

    l10n_in_pf_employee_contribution = fields.Float(string="Employee Contribution", default=12)
    l10n_in_pf_employer_contribution = fields.Float(string="Employer Contribution", default=12)
    l10n_in_professional_tax = fields.Monetary(string="Professional Tax", default=200)
    l10n_in_esic_employee_contribution = fields.Float(string="Employee Contribution", default=0.75)
    l10n_in_esic_employer_contribution = fields.Float(string="Employer Contribution", default=3.25)
    l10n_in_lwf_employee_contribution = fields.Monetary(string="Employee Contribution", currency_field="currency_id", default=6)
    l10n_in_lwf_employer_contribution = fields.Monetary(string="Employer Contribution", currency_field="currency_id", default=12)
    l10n_in_other_deduction = fields.Monetary(string="Other Deduction", currency_field="currency_id")

    @api.depends("l10n_in_basic_salary_percent", "wage")
    def _compute_l10n_in_basic_salary(self):
        for contract in self:
            contract.l10n_in_basic_salary = contract.wage * contract.l10n_in_basic_salary_percent

    def _inverse_l10n_in_basic_salary(self):
        for contract in self:
            contract.l10n_in_basic_salary_percent = contract.l10n_in_basic_salary / contract.wage if contract.wage else 0

    @api.depends("l10n_in_basic_salary", "l10n_in_house_rent_allowance_percent")
    def _compute_l10n_in_house_rent_allowance(self):
        for contract in self:
            contract.l10n_in_house_rent_allowance = contract.l10n_in_basic_salary * contract.l10n_in_house_rent_allowance_percent

    def _inverse_l10n_in_house_rent_allowance(self):
        for contract in self:
            contract.l10n_in_house_rent_allowance_percent = contract.l10n_in_house_rent_allowance / contract.l10n_in_basic_salary if contract.l10n_in_basic_salary else 0

    @api.depends("l10n_in_standard_allowance", "wage")
    def _compute_l10n_in_standard_allowance_percent(self):
        for contract in self:
            contract.l10n_in_standard_allowance_percent = contract.l10n_in_standard_allowance / contract.wage if contract.wage else 0

    def _inverse_l10n_in_standard_allowance_percent(self):
        for contract in self:
            contract.l10n_in_standard_allowance = contract.l10n_in_standard_allowance_percent * contract.wage

    @api.depends("l10n_in_performance_bonus_percent", "l10n_in_basic_salary")
    def _compute_l10n_in_performance_bonus(self):
        for contract in self:
            contract.l10n_in_performance_bonus = contract.l10n_in_basic_salary * contract.l10n_in_performance_bonus_percent

    def _inverse_l10n_in_performance_bonus(self):
        for contract in self:
            contract.l10n_in_performance_bonus_percent = contract.l10n_in_performance_bonus / contract.l10n_in_basic_salary if contract.l10n_in_basic_salary else 0

    @api.depends("l10n_in_leave_travel_allowance_percent", "l10n_in_basic_salary")
    def _compute_l10n_in_leave_travel_allowance(self):
        for contract in self:
            contract.l10n_in_leave_travel_allowance = contract.l10n_in_basic_salary * contract.l10n_in_leave_travel_allowance_percent

    def _inverse_l10n_in_leave_travel_allowance(self):
        for contract in self:
            contract.l10n_in_leave_travel_allowance_percent = contract.l10n_in_leave_travel_allowance / contract.l10n_in_basic_salary if contract.l10n_in_basic_salary else 0

    @api.depends('wage', 'l10n_in_leave_allowance_per_day_percent', 'l10n_in_leave_days')
    def _compute_leave_allowance(self):
        for contract in self:
            contract.l10n_in_leave_allowance = contract.wage * contract.l10n_in_leave_allowance_per_day_percent * contract.l10n_in_leave_days

    def _inverse_leave_allowance(self):
        for contract in self:
            if contract.l10n_in_basic_salary and contract.l10n_in_leave_days:
                contract.l10n_in_leave_allowance_percent = contract.l10n_in_leave_allowance / contract.wage if contract.wage else 0
                contract.l10n_in_leave_allowance_per_day_percent = contract.l10n_in_leave_allowance / (contract.wage * contract.l10n_in_leave_days) if contract.wage else 0

    @api.depends("l10n_in_gratuity", "l10n_in_basic_salary")
    def _compute_l10n_in_gratuity_percent(self):
        for contract in self:
            contract.l10n_in_gratuity_percent = contract.l10n_in_gratuity / contract.l10n_in_basic_salary if contract.l10n_in_basic_salary else 0

    def _inverse_l10n_in_gratuity_percent(self):
        for contract in self:
            contract.l10n_in_gratuity = contract.l10n_in_basic_salary * contract.l10n_in_gratuity_percent

    @api.depends("wage", "l10n_in_basic_salary", "l10n_in_house_rent_allowance", "l10n_in_standard_allowance", "l10n_in_performance_bonus", "l10n_in_leave_travel_allowance", "l10n_in_leave_allowance", "l10n_in_gratuity")
    def _compute_l10n_in_supplementary_allowance(self):
        for contract in self:
            total_allowance = sum([
                contract.l10n_in_basic_salary,
                contract.l10n_in_house_rent_allowance,
                contract.l10n_in_standard_allowance,
                contract.l10n_in_performance_bonus,
                contract.l10n_in_leave_travel_allowance,
                contract.l10n_in_leave_allowance,
                contract.l10n_in_gratuity
            ])
            if contract.wage:
                contract.l10n_in_supplementary_allowance = contract.wage - total_allowance

    def _inverse_l10n_in_supplementary_allowance(self):
        for contract in self:
            contract.l10n_in_supplementary_allowance_percent = contract.l10n_in_supplementary_allowance / contract.wage if contract.wage else 0
