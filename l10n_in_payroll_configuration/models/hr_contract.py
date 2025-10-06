from odoo import api, fields, models


class HrContract(models.Model):
    _inherit = 'hr.contract'

    _sql_constraints = [
        ('check_basic_salary_percent_positive', 'CHECK(l10n_in_basic_salary_percent >= 0)', 'Basic Salary cannot be negative.'),
        ('check_hra_percent_positive', 'CHECK(l10n_in_hra_percent >= 0)', 'HRA cannot be negative.'),
        ('check_performance_bonus_percent_positive', 'CHECK(l10n_in_performance_bonus_percent >= 0)', 'Performance Bonus cannot be negative.'),
        ('check_leave_travel_allowance_percent_positive', 'CHECK(l10n_in_leave_travel_allowance_percent >= 0)', 'Leave Travel Allowance cannot be negative.'),
        ('check_std_allowance_value_positive', 'CHECK(l10n_in_std_allowance >= 0)', 'Standard Allowance cannot be negative.'),
        ('check_leave_allowance_percent_positive', 'CHECK(l10n_in_leave_allowance_percent >= 0)', 'Leave Allowance cannot be negative.'),
        ('check_leave_days_positive', 'CHECK(l10n_in_leave_days >= 0)', 'Leave Days cannot be negative.'),
        ('check_pf_employee_contribution_positive', 'CHECK(l10n_in_pf_employee_contribution >= 0)', 'PF Employee Contribution cannot be negative.'),
        ('check_pf_employer_contribution_positive', 'CHECK(l10n_in_pf_employer_contribution >= 0)', 'PF Employer Contribution cannot be negative.'),
        ('check_esic_employee_contribution_positive', 'CHECK(l10n_in_esic_employee_contribution >= 0)', 'ESIC Employee Contribution cannot be negative.'),
        ('check_esic_employer_contribution_positive', 'CHECK(l10n_in_esic_employer_contribution >= 0)', 'ESIC Employer Contribution cannot be negative.'),
        ('check_lwf_employee_contribution_positive', 'CHECK(l10n_in_lwf_employee_contribution >= 0)', 'LWF Employee Contribution cannot be negative.'),
        ('check_lwf_employer_contribution_positive', 'CHECK(l10n_in_lwf_employer_contribution >= 0)', 'LWF Employer Contribution cannot be negative.'),
        ('check_prof_tax_value_positive', 'CHECK(l10n_in_professional_tax >= 0)', 'Professional Tax cannot be negative.'),
        ('check_other_deduction_positive', 'CHECK(l10n_in_other_deduction >= 0)', 'Other Deduction cannot be negative.'),
    ]

    # =======================================================
    #               SALARY COMPONENTS FIELDS
    # =======================================================

    l10n_in_basic_salary_percent = fields.Float(string="Basic Salary Percentage", default=50)
    l10n_in_basic_salary = fields.Monetary(
        string="Basic Salary",
        compute="_compute_l10n_in_basic_salary",
        inverse="_inverse_l10n_in_basic_salary",
        store=True,
        help="Fixed component of salary based on the wage and basic salary percentage."
    )

    l10n_in_hra_percent = fields.Float(string="House Rent Allowance Percentage", default=50)
    l10n_in_hra = fields.Monetary(
        string="House Rent Allowance",
        compute="_compute_l10n_in_hra",
        inverse="_inverse_l10n_in_hra",
        store=True,
        help="Allowance to cover housing expenses, calculated from basic salary and HRA percentage."
    )

    l10n_in_performance_bonus_percent = fields.Float(string="Performance Bonus Percentage", default=20)
    l10n_in_performance_bonus = fields.Monetary(
        string="Performance Bonus",
        compute="_compute_l10n_in_performance_bonus",
        inverse="_inverse_l10n_in_performance_bonus",
        store=True,
        help="Bonus amount based on performance, derived from basic salary and bonus percentage."
    )

    l10n_in_leave_travel_allowance_percent = fields.Float(string="Leave Travel Allowance Percentage", default=20)
    l10n_in_leave_travel_allowance = fields.Monetary(
        string="Leave Travel Allowance",
        compute="_compute_l10n_in_leave_travel_allowance",
        inverse="_inverse_l10n_in_leave_travel_allowance",
        store=True,
        help="Allowance for travel expenses during leave, based on basic salary and LTA percentage."
    )

    l10n_in_leave_days = fields.Integer(
        string="Leave Days",
        help="Number of leave days entitled per month.",
        default=1
    )

    l10n_in_std_allowance = fields.Monetary(
        string="Standard Allowance",
        help="Fixed allowance amount included in the salary structure.",
        default=4167
    )
    l10n_in_std_allowance_percent = fields.Float(
        string="Standard Allowance Percentage",
        compute="_compute_l10n_in_std_allowance_percent",
        inverse="_inverse_l10n_in_std_allowance_percent",
        store=True
    )

    l10n_in_gratuity = fields.Monetary(
        string="Gratuity Value",
        help="Amount set aside for gratuity, calculated from basic salary and gratuity percentage."
    )
    l10n_in_gratuity_percent = fields.Float(
        string="Gratuity Percentage",
        compute="_compute_l10n_in_gratuity_percent",
        inverse="_inverse_l10n_in_gratuity_percent",
        store=True
    )

    l10n_in_leave_allowance_percent = fields.Float(string="Leave Allowance Percentage")
    l10n_in_leave_allowance = fields.Monetary(
        string="Leave Allowance",
        compute="_compute_l10n_in_leave_allowance",
        inverse="_inverse_l10n_in_leave_allowance",
        store=True,
        help="Allowance for leaves, derived from wage and leave allowance percentage."
    )

    l10n_in_supplementary_allowance_percent = fields.Float(
        string="Supplementary Allowance Percentage",
        compute="_compute_l10n_in_supplementary_allowance_percent",
        inverse="_inverse_l10n_in_supplementary_allowance_percent"
    )
    l10n_in_supplementary_allowance = fields.Monetary(
        string="Supplementary Allowance",
        compute="_compute_l10n_in_supplementary_allowance",
        store=True,
        readonly=False,
        help="Residual amount of wage after allocating all other salary components."
    )

    # =======================================================
    #               OTHER DEDUCTIONS FIELDS
    # =======================================================

    l10n_in_pf_employee_contribution = fields.Float(
        string="PF Employee Contribution",
        default=lambda self: self.env.company.l10n_in_epf_employee_contri,
        help="Employee's contribution to Provident Fund (PF), deducted from salary."
    )
    l10n_in_pf_employer_contribution = fields.Float(
        string="PF Employer Contribution",
        default=lambda self: self.env.company.l10n_in_epf_employer_contri,
        help="Employer's contribution to Provident Fund (PF) for the employee."
    )
    l10n_in_esic_employee_contribution = fields.Float(
        string="ESIC Employee Contribution",
        default=lambda self: self.env.company.l10n_in_esic_employee_contri,
        help="Employee's contribution to Employee State Insurance (ESIC), deducted from salary."
    )
    l10n_in_esic_employer_contribution = fields.Float(
        string="ESIC Employer Contribution",
        default=lambda self: self.env.company.l10n_in_esic_employer_contri,
        help="Employer's contribution to Employee State Insurance (ESIC) for the employee."
    )
    l10n_in_lwf_employee_contribution = fields.Monetary(
        string="LWF Employee Contribution",
        default=lambda self: self.env.company.l10n_in_lwf_employee_contri,
        help="Employee's contribution to Labour Welfare Fund (LWF), deducted from salary."
    )
    l10n_in_lwf_employer_contribution = fields.Monetary(
        string="LWF Employer Contribution",
        default=lambda self: self.env.company.l10n_in_lwf_employer_contri,
        help="Employer's contribution to Labour Welfare Fund (LWF) for the employee."
    )
    l10n_in_professional_tax = fields.Monetary(string="Professional Tax", default=200, help="Fixed tax amount deducted from salary based on income slab.")
    l10n_in_other_deduction = fields.Monetary(string="Other Deduction", help="Additional deductions from salary not covered by other categories.")

    # =======================================================
    #                   COMPUTE METHODS
    # =======================================================

    @api.depends('wage','l10n_in_basic_salary_percent', 'hourly_wage', 'wage_type', 'resource_calendar_id',
    'resource_calendar_id.full_time_required_hours')
    def _compute_l10n_in_basic_salary(self):
        for record in self:
            wage = record.wage
            if record.wage_type == 'hourly':
                wage = record._convert_hourly_to_monthly(record.hourly_wage)
            record.l10n_in_basic_salary = wage * record.l10n_in_basic_salary_percent / 100.0

    @api.depends('l10n_in_basic_salary','l10n_in_hra_percent')
    def _compute_l10n_in_hra(self):
        for record in self:
            record.l10n_in_hra = record.l10n_in_basic_salary * record.l10n_in_hra_percent / 100.0

    @api.depends('l10n_in_basic_salary','l10n_in_performance_bonus_percent')
    def _compute_l10n_in_performance_bonus(self):
        for record in self:
            record.l10n_in_performance_bonus = record.l10n_in_basic_salary * record.l10n_in_performance_bonus_percent / 100.0

    @api.depends('l10n_in_basic_salary','l10n_in_leave_travel_allowance_percent')
    def _compute_l10n_in_leave_travel_allowance(self):
        for record in self:
            record.l10n_in_leave_travel_allowance = record.l10n_in_basic_salary * record.l10n_in_leave_travel_allowance_percent / 100.0

    @api.depends('wage', 'l10n_in_std_allowance', 'hourly_wage', 'wage_type', 'resource_calendar_id',
    'resource_calendar_id.full_time_required_hours')
    def _compute_l10n_in_std_allowance_percent(self):
        for record in self:
            wage = record.wage
            if record.wage_type == 'hourly':
                wage = record._convert_hourly_to_monthly(record.hourly_wage)
            record.l10n_in_std_allowance_percent = record.l10n_in_std_allowance * 100.0 / wage if wage else 0.0

    @api.depends("l10n_in_basic_salary", "l10n_in_gratuity")
    def _compute_l10n_in_gratuity_percent(self):
        for record in self:
            if record.l10n_in_basic_salary:
                record.l10n_in_gratuity_percent = record.l10n_in_gratuity * 100.0 / record.l10n_in_basic_salary
            else:
                record.l10n_in_gratuity_percent = 0.0

    @api.depends('wage','l10n_in_leave_allowance_percent', 'hourly_wage', 'wage_type', 'resource_calendar_id',
    'resource_calendar_id.full_time_required_hours')
    def _compute_l10n_in_leave_allowance(self):
        for record in self:
            wage = record.wage
            if record.wage_type == 'hourly':
                wage = record._convert_hourly_to_monthly(record.hourly_wage)
            if wage:
                record.l10n_in_leave_allowance = wage * record.l10n_in_leave_allowance_percent / 100.0

    @api.depends("wage", "l10n_in_basic_salary", "l10n_in_hra", "l10n_in_std_allowance_percent",
    "l10n_in_performance_bonus", "l10n_in_leave_travel_allowance", "l10n_in_leave_allowance",
    "l10n_in_gratuity_percent", 'hourly_wage', 'wage_type', 'resource_calendar_id', 'resource_calendar_id.full_time_required_hours')
    def _compute_l10n_in_supplementary_allowance(self):
        supplementary_allowance_set_default_val = self.env['res.config.settings'].default_get(['default_l10n_in_supplementary_allowance']).get('default_l10n_in_supplementary_allowance')
        for record in self:
            if supplementary_allowance_set_default_val == 0.0 or record.l10n_in_supplementary_allowance != supplementary_allowance_set_default_val:
                wage = record.wage
                if record.wage_type == 'hourly':
                    wage = record._convert_hourly_to_monthly(record.hourly_wage)
                total = sum([
                    record.l10n_in_basic_salary,
                    record.l10n_in_hra,
                    record.l10n_in_performance_bonus,
                    record.l10n_in_leave_travel_allowance,
                    record.l10n_in_leave_allowance,
                    (wage * record.l10n_in_std_allowance_percent / 100.0),
                    (record.l10n_in_basic_salary * record.l10n_in_gratuity_percent / 100.0)
                ])
                record.l10n_in_supplementary_allowance = wage - total

    @api.depends('l10n_in_supplementary_allowance')
    def _compute_l10n_in_supplementary_allowance_percent(self):
        for record in self:
            wage = record.wage
            if record.wage_type == 'hourly':
                wage = record._convert_hourly_to_monthly(record.hourly_wage)
            if wage:
                record.l10n_in_supplementary_allowance_percent = record.l10n_in_supplementary_allowance * 100.0 / wage

    # =======================================================
    #                   INVERSE METHODS
    # =======================================================

    def _inverse_l10n_in_basic_salary(self):
        for record in self:
            wage = record.wage
            if record.wage_type == 'hourly':
                wage = record._convert_hourly_to_monthly(record.hourly_wage)
            if wage:
                record.l10n_in_basic_salary_percent = record.l10n_in_basic_salary * 100.0 / wage

    def _inverse_l10n_in_hra(self):
        for record in self:
            if record.l10n_in_basic_salary:
                record.l10n_in_hra_percent = record.l10n_in_hra * 100.0 / record.l10n_in_basic_salary

    def _inverse_l10n_in_performance_bonus(self):
        for record in self:
            if record.l10n_in_basic_salary:
                record.l10n_in_performance_bonus_percent = record.l10n_in_performance_bonus * 100.0 / record.l10n_in_basic_salary

    def _inverse_l10n_in_leave_travel_allowance(self):
        for record in self:
            if record.l10n_in_basic_salary:
                record.l10n_in_leave_travel_allowance_percent = record.l10n_in_leave_travel_allowance * 100.0 / record.l10n_in_basic_salary

    def _inverse_l10n_in_std_allowance_percent(self):
        for record in self:
            wage = record.wage
            if record.wage_type == 'hourly':
                wage = record._convert_hourly_to_monthly(record.hourly_wage)
            if wage:
                record.l10n_in_std_allowance = wage * record.l10n_in_std_allowance_percent / 100.0

    def _inverse_l10n_in_gratuity_percent(self):
        for record in self:
            record.l10n_in_gratuity = record.l10n_in_basic_salary * record.l10n_in_gratuity_percent / 100.0

    def _inverse_l10n_in_leave_allowance(self):
        for record in self:
            wage = record.wage
            if record.wage_type == 'hourly':
                wage = record._convert_hourly_to_monthly(record.hourly_wage)
            if wage:
                record.l10n_in_leave_allowance_percent = record.l10n_in_leave_allowance * 100.0 / wage

    def _inverse_l10n_in_supplementary_allowance_percent(self):
        for record in self:
            wage = record.wage
            if record.wage_type == 'hourly':
                wage = record._convert_hourly_to_monthly(record.hourly_wage)
            if wage:
                record.l10n_in_supplementary_allowance = record.l10n_in_supplementary_allowance_percent * wage / 100.0

    # =======================================================
    #              HOURLY TYPE WAGE CALCULATION
    # =======================================================

    def _convert_hourly_to_monthly(self, hourly_wage):
        reqd_hours = self.resource_calendar_id.full_time_required_hours
        return reqd_hours * 4 * hourly_wage
