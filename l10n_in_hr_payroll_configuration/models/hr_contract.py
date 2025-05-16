from odoo import api, fields, models


class HrContract(models.Model):
    _inherit = "hr.contract"

    l10n_in_basic_salary = fields.Monetary(string="Basic Salary", compute="_compute_basic_salary", inverse="_inverse_basic_salary", readonly=False)
    l10n_in_hra = fields.Monetary(string="House Rent Allowance", compute="_compute_hra", inverse="_inverse_hra", readonly=False)
    l10n_in_performance_bonus = fields.Monetary(string="Performance Bonus", compute="_compute_performance_bonus", inverse="_inverse_performance_bonus", readonly=False)
    l10n_in_supp_allowance = fields.Monetary(string="Supplementary Allowance", compute="_compute_supp_allowance", readonly=False)
    l10n_in_leave_travel_allowance = fields.Monetary(string="Leave Travel Allowance", compute="_compute_leave_travel_allowance", inverse="_inverse_leave_travel_allowance", readonly=False)
    l10n_in_leave_allowance = fields.Monetary(string="Leave Allowance", readonly=False)
    l10n_in_leave_allowance_per_day = fields.Monetary(readonly=True)
    l10n_in_gratuity = fields.Monetary(string="Gratuity", compute="_compute_gratuity", inverse="_inverse_gratuity", readonly=False)
    l10n_in_pt = fields.Monetary(string="Professional Tax", readonly=False, default=200)
    l10n_in_per_day_allowance = fields.Monetary(store=True, default=0.0)

    l10n_in_provident_fund_company = fields.Boolean(string="Employees' Provident Fund", store=True, readonly=False)
    l10n_in_pf_employer_contribution_company = fields.Float(string="PF Employer Contribution", store=True, readonly=False)
    l10n_in_pf_employee_contribution_company = fields.Float(string="PF Employee Contribution", store=True, readonly=False)
    l10n_in_esic_company = fields.Boolean(string="Employees' State Insurance Corporation", store=True, readonly=False)
    l10n_in_esic_employee_contribution_company = fields.Float(string="ESIC Employee Contribution", store=True, readonly=False)
    l10n_in_esic_employer_contribution_company = fields.Float(string="ESIC Employer Contribution",  store=True, readonly=False)
    l10n_in_professional_tax_company = fields.Boolean(string="Professional Tax",  store=True, readonly=False)
    l10n_in_lwf_company = fields.Boolean(string="Labour Welfare Fund", store=True, readonly=False)
    l10n_in_lwf_employee_contribution_company = fields.Monetary(string="LWF Employee Contribution",store=True, readonly=False)
    l10n_in_lwf_employer_contribution_company = fields.Monetary(string="LWF Employer Contribution", store=True, readonly=False)
    l10n_in_other_deductions = fields.Monetary(string="Other Deductions", readonly=False)

    l10n_in_basic_salary_company = fields.Float()
    l10n_in_hra_company = fields.Float()
    l10n_in_standard_allowance = fields.Monetary(string="Standard Allowance")
    l10n_in_performance_bonus_company = fields.Float()
    l10n_in_leave_allowance_company = fields.Float()
    l10n_in_leave_days_company = fields.Integer(string="Leave Days")
    l10n_in_gratuity_company = fields.Float()

    l10n_in_leave_allowance_percent = fields.Float(readonly=True, compute="_compute_leave_allowance_percent")
    l10n_in_supp_allowance_percent = fields.Float(readonly=False, compute="_compute_supp_percent", inverse="_inverse_supp_allowance")
    l10n_in_standard_allowance_percent = fields.Float(compute="_compute_standard_allowance_perc", inverse="_inverse_standard_allowance_percent", readonly=False)

    @api.depends("l10n_in_basic_salary_company", "wage")
    def _compute_basic_salary(self):
        for contract in self:
            if contract.wage:
                contract.l10n_in_basic_salary = contract.l10n_in_basic_salary_company * contract.wage

    def _inverse_basic_salary(self):
        for contract in self:
            if contract.wage:
                contract.l10n_in_basic_salary_company = contract.l10n_in_basic_salary / contract.wage

    @api.depends("l10n_in_hra_company", "l10n_in_basic_salary")
    def _compute_hra(self):
        for contract in self:
            if contract.wage:
                contract.l10n_in_hra = contract.l10n_in_hra_company * contract.l10n_in_basic_salary

    def _inverse_hra(self):
        for contract in self:
            if contract.wage:
                contract.l10n_in_hra_company = contract.l10n_in_hra / contract.l10n_in_basic_salary

    @api.depends("l10n_in_performance_bonus_company","l10n_in_basic_salary")
    def _compute_performance_bonus(self):
        for contract in self:
            if contract.wage:
                contract.l10n_in_performance_bonus = contract.l10n_in_performance_bonus_company * contract.l10n_in_basic_salary

    def _inverse_performance_bonus(self):
        for contract in self:
            if contract.wage:
                contract.l10n_in_performance_bonus_company = contract.l10n_in_performance_bonus / contract.l10n_in_basic_salary

    @api.depends("l10n_in_leave_allowance_company","l10n_in_basic_salary")
    def _compute_leave_travel_allowance(self):
        for contract in self:
            if contract.wage:
                contract.l10n_in_leave_travel_allowance = contract.l10n_in_leave_allowance_company * contract.l10n_in_basic_salary

    def _inverse_leave_travel_allowance(self):
        for contract in self:
            if contract.wage:
                contract.l10n_in_leave_allowance_company = contract.l10n_in_leave_travel_allowance / contract.l10n_in_basic_salary

    @api.onchange('l10n_in_leave_days_company')
    def _onchange_leave_days_company(self):
        self.l10n_in_leave_allowance = self.l10n_in_leave_days_company * self.l10n_in_per_day_allowance

    @api.onchange('l10n_in_leave_allowance')
    def _onchange_leave_allowance(self):
        if self.l10n_in_leave_days_company > 0:
            self.l10n_in_per_day_allowance = self.l10n_in_leave_allowance / self.l10n_in_leave_days_company

    @api.depends("wage","l10n_in_leave_allowance")
    def _compute_leave_allowance_percent(self):
        for contract in self:
            if contract.wage:
                contract.l10n_in_leave_allowance_percent = contract.l10n_in_leave_allowance / contract.wage
            else:
                contract.l10n_in_leave_allowance_percent = 0

    @api.depends("l10n_in_gratuity_company","l10n_in_basic_salary")
    def _compute_gratuity(self):
        for contract in self:
            if contract.wage:
                contract.l10n_in_gratuity = contract.l10n_in_gratuity_company * contract.l10n_in_basic_salary

    def _inverse_gratuity(self):
        for contract in self:
            if contract.wage and contract.l10n_in_basic_salary:
                contract.l10n_in_gratuity_company = contract.l10n_in_gratuity / contract.l10n_in_basic_salary

    @api.depends("wage","l10n_in_standard_allowance")
    def _compute_standard_allowance_perc(self):
        for contract in self:
            if contract.wage:
                contract.l10n_in_standard_allowance_percent = contract.l10n_in_standard_allowance / contract.wage

    def _inverse_standard_allowance_percent(self):
        for contract in self:
            if contract.wage:
                contract.l10n_in_standard_allowance = contract.l10n_in_standard_allowance_percent * contract.wage

    @api.depends(
        "wage",
        "l10n_in_basic_salary",
        "l10n_in_hra",
        "l10n_in_standard_allowance",
        "l10n_in_performance_bonus",
        "l10n_in_leave_travel_allowance",
        "l10n_in_leave_allowance",
        "l10n_in_gratuity",
    )
    def _compute_supp_allowance(self):
        for contract in self:
            if contract.wage:
                total_components = (
                    contract.l10n_in_basic_salary
                    + contract.l10n_in_hra
                    + contract.l10n_in_standard_allowance
                    + contract.l10n_in_performance_bonus
                    + contract.l10n_in_leave_travel_allowance
                    + contract.l10n_in_leave_allowance
                    + contract.l10n_in_gratuity
                )
                contract.l10n_in_supp_allowance = contract.wage - total_components
            else:
                contract.l10n_in_supp_allowance = 0.0

    @api.depends("wage","l10n_in_supp_allowance")
    def _compute_supp_percent(self):
        for contract in self:
            if contract.wage:
                contract.l10n_in_supp_allowance_percent = contract.l10n_in_supp_allowance / contract.wage
            else:
                contract.l10n_in_supp_allowance_percent = 0

    def _inverse_supp_allowance(self):
        for contract in self:
            if contract.wage:
                contract.l10n_in_supp_allowance = contract.l10n_in_supp_allowance_percent * contract.wage
