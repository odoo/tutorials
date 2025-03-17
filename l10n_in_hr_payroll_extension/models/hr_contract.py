from odoo import api, fields, models


class HrContract(models.Model):
    _inherit = 'hr.contract'

    l10n_in_basic_salary = fields.Float(string="Basic Salary", help="Basic salary calculated from the wage", compute="_compute_l10n_in_basic_salary", inverse="_inverse_l10n_in_basic_salary")
    l10n_in_house_rent_allowance = fields.Float(string="House Rent Allowance", compute="_compute_l10n_in_house_rent_allowance", inverse="_inverse_l10n_in_house_rent_allowance")
    l10n_in_standard_allowance = fields.Float(string="Standard Allowance", default=4167)
    l10n_in_performance_bonus = fields.Float(string="Performance Bonus", compute="_compute_l10n_in_performance_bonus", inverse="_inverse_l10n_in_performance_bonus")
    l10n_in_leave_travel_allowance = fields.Float(string="Leave Travel Allowance", compute="_compute_l10n_in_leave_travel_allowance", inverse="_inverse_l10n_in_leave_travel_allowance")
    l10n_in_leave_allowance = fields.Float(string="Leave Allowance", compute="_compute_leave_allowance", inverse="_inverse_leave_allowance")
    l10n_in_leave_days = fields.Float(string="Leave Days", default=1)
    l10n_in_gratuity = fields.Float(string="Gratuity", default=0)
    l10n_in_supplementary_allowance = fields.Float(string="Supplementary Allowance", compute="_compute_l10n_in_supplementary_allowance", inverse="_inverse_l10n_in_supplementary_allowance", default=0)

    l10n_in_basic_salary_percent = fields.Float(string="Basic Salary Percentage", help="basic salary percentage of wage", default=50)
    l10n_in_house_rent_allowance_percent = fields.Float(string="House Rent Allowance Percentage", help="this is the percentage of basic salary", default=50)
    l10n_in_standard_allowance_percent = fields.Float(string="Standard Allowance Percentage", compute="_compute_l10n_in_standard_allowance_percent", inverse="_inverse_l10n_in_standard_allowance_percent")
    l10n_in_performance_bonus_percent = fields.Float(string="Performance Bonus Percentage", default=20)
    l10n_in_leave_travel_allowance_percent = fields.Float(string="Leave Travel Allowance Percentage", default=20)
    l10n_in_leave_allowance_per_day_percent = fields.Float(string="Leave allowance per day percentage")
    l10n_in_leave_allowance_percent = fields.Float(string="Leave Allowance Percentage")
    l10n_in_gratuity_percent = fields.Float(string="Gratuity Percentage", compute="_compute_l10n_in_gratuity_percent", inverse="_inverse_l10n_in_gratuity_percent")
    l10n_in_supplementary_allowance_percent = fields.Float(string="Supplementary Allowance Percentage")

    l10n_in_pf_employee_contribution = fields.Float(related="company_id.l10n_in_pf_employee_contribution", readonly=False)
    l10n_in_pf_employer_contribution = fields.Float(related="company_id.l10n_in_pf_employer_contribution", readonly=False)
    l10n_in_professional_tax = fields.Float(string="Professional Tax", default=200)
    l10n_in_esic_employee_contribution = fields.Float(related="company_id.l10n_in_esic_employee_contribution", readonly=False)
    l10n_in_esic_employer_contribution = fields.Float(related="company_id.l10n_in_esic_employer_contribution", readonly=False)
    l10n_in_lwf_employee_contribution = fields.Float(related="company_id.l10n_in_lwf_employee_contribution", readonly=False)
    l10n_in_lwf_employer_contribution = fields.Float(related="company_id.l10n_in_lwf_employer_contribution", readonly=False)
    l10n_in_other_deduction = fields.Float(string="Other Deduction")

    @api.depends("l10n_in_basic_salary_percent", "wage")
    def _compute_l10n_in_basic_salary(self):
        for record in self:
            record.l10n_in_basic_salary = record.wage * (record.l10n_in_basic_salary_percent / 100)

    def _inverse_l10n_in_basic_salary(self):
        for record in self:
            record.l10n_in_basic_salary_percent = (record.l10n_in_basic_salary * 100) / record.wage if record.wage else 0

    @api.depends("l10n_in_basic_salary", "l10n_in_house_rent_allowance_percent")
    def _compute_l10n_in_house_rent_allowance(self):
        for record in self:
            record.l10n_in_house_rent_allowance = record.l10n_in_basic_salary * (record.l10n_in_house_rent_allowance_percent / 100)

    def _inverse_l10n_in_house_rent_allowance(self):
        for record in self:
            record.l10n_in_house_rent_allowance_percent = (record.l10n_in_house_rent_allowance * 100) / record.l10n_in_basic_salary if record.l10n_in_basic_salary else 0

    @api.depends("l10n_in_standard_allowance", "wage")
    def _compute_l10n_in_standard_allowance_percent(self):
        for record in self:
            record.l10n_in_standard_allowance_percent = (record.l10n_in_standard_allowance * 100) / record.wage if record.wage else 0

    def _inverse_l10n_in_standard_allowance_percent(self):
        for record in self:
            record.l10n_in_standard_allowance = (record.l10n_in_standard_allowance_percent * record.wage) / 100

    @api.depends("l10n_in_performance_bonus_percent", "l10n_in_basic_salary")
    def _compute_l10n_in_performance_bonus(self):
        for record in self:
            record.l10n_in_performance_bonus = record.l10n_in_basic_salary * (record.l10n_in_performance_bonus_percent / 100)

    def _inverse_l10n_in_performance_bonus(self):
        for record in self:
            record.l10n_in_performance_bonus_percent = (record.l10n_in_performance_bonus * 100) / record.l10n_in_basic_salary if record.l10n_in_basic_salary else 0

    @api.depends("l10n_in_leave_travel_allowance_percent", "l10n_in_basic_salary")
    def _compute_l10n_in_leave_travel_allowance(self):
        for record in self:
            record.l10n_in_leave_travel_allowance = record.l10n_in_basic_salary * (record.l10n_in_leave_travel_allowance_percent / 100)

    def _inverse_l10n_in_leave_travel_allowance(self):
        for record in self:
            record.l10n_in_leave_travel_allowance_percent = record.l10n_in_leave_days * ((record.l10n_in_leave_allowance * 100) / record.wage if record.wage else 0)

    @api.depends('wage', 'l10n_in_leave_allowance_per_day_percent', 'l10n_in_leave_days')
    def _compute_leave_allowance(self):
        for record in self:
            record.l10n_in_leave_allowance = (record.wage * (record.l10n_in_leave_allowance_per_day_percent/100) * record.l10n_in_leave_days)

    def _inverse_leave_allowance(self):
        for record in self:
            if record.l10n_in_basic_salary and record.l10n_in_leave_days:
                record.l10n_in_leave_allowance_percent = record.l10n_in_leave_allowance * 100 / record.wage if record.wage else 0
                record.l10n_in_leave_allowance_per_day_percent = (record.l10n_in_leave_allowance * 100 / (record.wage * record.l10n_in_leave_days)) if record.wage else 0

    @api.depends("l10n_in_gratuity", "l10n_in_basic_salary")
    def _compute_l10n_in_gratuity_percent(self):
        for record in self:
            record.l10n_in_gratuity_percent = (record.l10n_in_gratuity * 100) / record.l10n_in_basic_salary if record.l10n_in_basic_salary else 0

    def _inverse_l10n_in_gratuity_percent(self):
        for record in self:
            record.l10n_in_gratuity = record.l10n_in_basic_salary * (record.l10n_in_gratuity_percent / 100)

    @api.depends("wage", "l10n_in_basic_salary", "l10n_in_house_rent_allowance", "l10n_in_standard_allowance", "l10n_in_performance_bonus", "l10n_in_leave_travel_allowance", "l10n_in_leave_allowance", "l10n_in_gratuity")
    def _compute_l10n_in_supplementary_allowance(self):
        for record in self:
            total_allowance = sum([
                record.l10n_in_basic_salary,
                record.l10n_in_house_rent_allowance,
                record.l10n_in_standard_allowance,
                record.l10n_in_performance_bonus,
                record.l10n_in_leave_travel_allowance,
                record.l10n_in_leave_allowance,
                record.l10n_in_gratuity
            ])
            if record.wage:
                record.l10n_in_supplementary_allowance = record.wage - total_allowance

    def _inverse_l10n_in_supplementary_allowance(self):
        for record in self:
            record.l10n_in_supplementary_allowance_percent = (record.l10n_in_supplementary_allowance * 100) / record.wage if record.wage else 0
