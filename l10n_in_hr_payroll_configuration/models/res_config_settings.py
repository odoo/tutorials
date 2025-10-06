from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    currency_id = fields.Many2one(
        string="Currency", related="company_id.currency_id", readonly=True
    )
    currency_symbol = fields.Char(related="currency_id.symbol")
    default_l10n_in_provident_fund_company = fields.Boolean(
        string="Employees' Provident Fund",
        default_model = "hr.contract"
    )
    l10n_in_pf_employer_identification = fields.Char(
        string="Employer Identification",
        related="company_id.l10n_in_pf_employer_identification",
        readonly=False,
    )
    default_l10n_in_pf_employee_contribution_company = fields.Float(
        string="Employee Contribution",
        default_model = "hr.contract"
    )
    default_l10n_in_pf_employer_contribution_company = fields.Float(
        string="Employer Contribution",
        default_model = "hr.contract"
    )

    default_l10n_in_esic_company = fields.Boolean(
        string="Employees' State Insurance Corporation",
        default_model = "hr.contract"
    )
    l10n_in_esic_ip = fields.Char(
        string="ESIC IP", related="company_id.l10n_in_esic_ip", readonly=False
    )
    default_l10n_in_esic_employee_contribution_company = fields.Float(
        string="Employee Contribution",
        default_model = "hr.contract"
    )
    default_l10n_in_esic_employer_contribution_company = fields.Float(
        string="Employer Contribution",
        default_model = "hr.contract"
    )

    default_l10n_in_professional_tax_company = fields.Boolean(
        string="Professional Tax",
        default_model = "hr.contract"
    )
    l10n_in_pt_number = fields.Char(
        string="Professional Tax Number",
        related="company_id.l10n_in_pt_number",
        readonly=False,
    )
    default_l10n_in_lwf_company = fields.Boolean(
        string="Labour Welfare Fund", default_model = "hr.contract"
    )
    default_l10n_in_lwf_employee_contribution_company = fields.Monetary(
        string="Employee's Contribution",
        default_model = "hr.contract"
    )
    default_l10n_in_lwf_employer_contribution_company = fields.Monetary(
        string="Employer's Contribution",
        default_model = "hr.contract"
    )

    default_l10n_in_basic_salary_company = fields.Float(string="Basic Salary", default_model="hr.contract")
    default_l10n_in_hra_company = fields.Float(string="House Rent Allowance", default_model="hr.contract")
    default_l10n_in_standard_allowance = fields.Monetary(string="Standard Allowance", default_model="hr.contract")
    default_l10n_in_performance_bonus_company = fields.Float(
        string="Performance Bonus",
        default_model="hr.contract"
    )
    default_l10n_in_leave_allowance_company = fields.Float(
        string="Leave Travel Allowance",
        default_model="hr.contract"
    )
    default_l10n_in_leave_days_company = fields.Integer(
        string="Leave Days", default_model="hr.contract"
    )
    default_l10n_in_gratuity_company = fields.Float(
        string="Gratuity", default_model="hr.contract"
    )
    default_l10n_in_supp_allowance = fields.Float(
        string="Supplementary Allowance",
        default_model="hr.contract"
    )
    l10n_in_organization_tax_details = fields.Boolean(
        string="Organization Tax Details",
        related="company_id.l10n_in_organization_tax_details",
        readonly=False,
    )
    l10n_in_tan_number = fields.Char(
        string="TAN Number",
        related="company_id.l10n_in_tan_number",
        readonly=False,
    )
    l10n_in_pan_number = fields.Char(
        string="PAN Number",
        related="company_id.l10n_in_pan_number",
        readonly=False,
    )
    l10n_in_tds_circle = fields.Char(
        string="TDS Cirle / AO code",
        related="company_id.l10n_in_tds_circle",
        readonly=False,
    )
