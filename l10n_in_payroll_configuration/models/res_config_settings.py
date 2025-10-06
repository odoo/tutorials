from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    _sql_constraints = [
        ('check_basic_salary_percent_positive', 'CHECK(default_l10n_in_basic_salary_percent >= 0)', "Basic Salary Percentage cannot be negative."),
        ('check_hra_percent_positive', 'CHECK(default_l10n_in_hra_percent >= 0)', "House Rent Allowance (HRA) Percentage cannot be negative."),
        ('check_std_allowance_positive', 'CHECK(default_l10n_in_std_allowance >= 0)', "Standard Allowance cannot be negative."),
        ('check_performance_bonus_percent_positive', 'CHECK(default_l10n_in_performance_bonus_percent >= 0)', "Performance Bonus Percentage cannot be negative."),
        ('check_lta_percent_positive', 'CHECK(default_l10n_in_leave_travel_allowance_percent >= 0)', "Leave Travel Allowance Percentage cannot be negative."),
        ('check_leaves_per_month_positive', 'CHECK(default_l10n_in_leave_days >= 0)', "Leave Days per Month cannot be negative."),
        ('check_gratuity_positive', 'CHECK(default_l10n_in_gratuity >= 0)', "Gratuity cannot be negative."),
    ]

    company_currency_id = fields.Many2one(string="Company Currency", related='company_id.currency_id')

    l10n_in_org_tax_details = fields.Boolean(related='company_id.l10n_in_org_tax_details', readonly=False)
    l10n_in_org_pan_number = fields.Char(related='company_id.l10n_in_org_pan_number', readonly=False)
    l10n_in_org_tan_number = fields.Char(related='company_id.l10n_in_org_tan_number', readonly=False)
    l10n_in_org_tds_circle_number = fields.Char(related='company_id.l10n_in_org_tds_circle_number', readonly=False)

    l10n_in_epf = fields.Boolean(related='company_id.l10n_in_epf', readonly=False)
    l10n_in_epf_employer_id = fields.Char(related='company_id.l10n_in_epf_employer_id', readonly=False)
    l10n_in_epf_employee_contri = fields.Float(related='company_id.l10n_in_epf_employee_contri', readonly=False)
    l10n_in_epf_employer_contri = fields.Float(related='company_id.l10n_in_epf_employer_contri', readonly=False)

    l10n_in_prof_tax = fields.Boolean(related='company_id.l10n_in_prof_tax', readonly=False)
    l10n_in_prof_tax_number = fields.Char(related='company_id.l10n_in_prof_tax_number', readonly=False)

    l10n_in_esic = fields.Boolean(related='company_id.l10n_in_esic', readonly=False)
    l10n_in_esic_ip_number = fields.Char(related='company_id.l10n_in_esic_ip_number', readonly=False)
    l10n_in_esic_employee_contri = fields.Float(related='company_id.l10n_in_esic_employee_contri', readonly=False)
    l10n_in_esic_employer_contri = fields.Float(related='company_id.l10n_in_esic_employer_contri', readonly=False)

    l10n_in_lwf = fields.Boolean(related='company_id.l10n_in_lwf', readonly=False)
    l10n_in_lwf_employee_contri = fields.Monetary(related='company_id.l10n_in_lwf_employee_contri', readonly=False, currency_field='company_currency_id')
    l10n_in_lwf_employer_contri = fields.Monetary(related='company_id.l10n_in_lwf_employer_contri', readonly=False, currency_field='company_currency_id')

    default_l10n_in_basic_salary_percent = fields.Float(
        string="Basic Salary",
        default_model="hr.contract")
    default_l10n_in_hra_percent = fields.Float(
        string="House Rent Allowance",
        default_model="hr.contract")
    default_l10n_in_performance_bonus_percent = fields.Float(
        string="Performance Bonus",
        default_model="hr.contract")
    default_l10n_in_leave_travel_allowance_percent = fields.Float(
        string="Leave Travel Allowance",
        default_model="hr.contract")
    default_l10n_in_std_allowance = fields.Float(
        string="Standard Allowance",
        default_model="hr.contract")
    default_l10n_in_leave_days = fields.Integer(
        string="Leave Days",
        default_model="hr.contract")
    default_l10n_in_gratuity = fields.Float(
        string="Gratuity Amount",
        default_model="hr.contract")
    default_l10n_in_supplementary_allowance = fields.Float(
        string="Supplementary Allowance",
        default_model="hr.contract")
