from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id)

    l10n_in_org_tax_details = fields.Boolean(related='company_id.l10n_in_org_tax_details', readonly=False)
    l10n_in_org_pan_number = fields.Char(related='company_id.l10n_in_org_pan_number', readonly=False)
    l10n_in_org_tan_number = fields.Char(related='company_id.l10n_in_org_tan_number', readonly=False)
    l10n_in_org_tds_circle = fields.Char(related='company_id.l10n_in_org_tds_circle', readonly=False)

    l10n_in_is_provident_fund = fields.Boolean(string="Employee's Provident Fund", default=True)
    l10n_in_employer_identification = fields.Char(related='company_id.l10n_in_employer_identification', readonly=False)
    default_l10n_in_pf_employee_contribution = fields.Float(string="Employee Contribution", default_model="hr.contract", default=12)
    default_l10n_in_pf_employer_contribution = fields.Float(string="Employer Contribution", default_model="hr.contract", default=12)

    l10n_in_is_professional_tax = fields.Boolean(string="Professional Tax", default=True)
    l10n_in_professional_tax_number = fields.Char(related='company_id.l10n_in_professional_tax_number', readonly=False)

    l10n_in_is_esic = fields.Boolean(string="Employee's State Insurance Corporation", default=True)
    l10n_in_esic_ip = fields.Char(related='company_id.l10n_in_esic_ip', readonly=False)
    default_l10n_in_esic_employee_contribution = fields.Float(string="Employee Contribution", default_model="hr.contract", default=0.75)
    default_l10n_in_esic_employer_contribution = fields.Float(string="Employer Contribution", default_model="hr.contract", default=3.25)

    l10n_in_is_lwf = fields.Boolean(string="Labour Welfare Fund", default=True)
    default_l10n_in_lwf_employee_contribution = fields.Monetary(string="Employee Contribution", currency_field="currency_id", default_model="hr.contract", default=6)
    default_l10n_in_lwf_employer_contribution = fields.Monetary(string="Employer Contribution", currency_field="currency_id", default_model="hr.contract", default=12)

    default_l10n_in_basic_salary_percent = fields.Float(string="Basic Salary", help="You can define the % of the salary from company cost to compute the basic salary based on your wages (Including D4).", default_model="hr.contract", default=50)
    default_l10n_in_house_rent_allowance_percent = fields.Float(string="House Rent Allowance", help="You can define 50% for metro city and 40% for non-metro city.", default_model="hr.contract", default=50)
    default_l10n_in_standard_allowance = fields.Float(string="Standard Allowance", default_model="hr.contract", default=4167)
    default_l10n_in_performance_bonus_percent = fields.Float(string="Performance Bonus", default_model="hr.contract", default=20)
    default_l10n_in_leave_travel_allowance_percent = fields.Float(string="Leave Travel Allowance", default_model="hr.contract", default=20)
    default_l10n_in_leave_days = fields.Float(string="Leave Days", default_model="hr.contract", default=1)
    default_l10n_in_gratuity = fields.Float(string="Gratuity", default_model="hr.contract")
    default_l10n_in_supplementary_allowance = fields.Float(string="Supplementary Allowance", default_model="hr.contract")
