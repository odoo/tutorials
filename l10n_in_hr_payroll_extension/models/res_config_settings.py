from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id)

    l10n_in_org_tax_details = fields.Boolean(related='company_id.l10n_in_org_tax_details', readonly=False)
    l10n_in_org_pan_number = fields.Char(related='company_id.l10n_in_org_pan_number', readonly=False)
    l10n_in_org_tan_number = fields.Char(related='company_id.l10n_in_org_tan_number', readonly=False)
    l10n_in_org_tds_circle = fields.Char(related='company_id.l10n_in_org_tds_circle', readonly=False)

    l10n_in_is_provident_fund = fields.Boolean(string="Employee's Provident Fund", default=True)
    l10n_in_pf_employer_identification = fields.Char(related='company_id.l10n_in_pf_employer_identification', readonly=False)
    l10n_in_pf_employee_contribution = fields.Float(related="company_id.l10n_in_pf_employee_contribution", readonly=False)
    l10n_in_pf_employer_contribution = fields.Float(related="company_id.l10n_in_pf_employer_contribution", readonly=False)

    l10n_in_is_professional_tax = fields.Boolean(string="Professional Tax", default=True)
    l10n_in_professional_tax_number = fields.Char(related='company_id.l10n_in_professional_tax_number', readonly=False)

    l10n_in_is_esic = fields.Boolean(string="Employee's State Insurance Corporation", default=True)
    l10n_in_esic_ip = fields.Char(string="ESIC IP", related='company_id.l10n_in_esic_ip', readonly=False)
    l10n_in_esic_employee_contribution = fields.Float(related="company_id.l10n_in_esic_employee_contribution", readonly=False)
    l10n_in_esic_employer_contribution = fields.Float(related="company_id.l10n_in_esic_employer_contribution", readonly=False)

    l10n_in_is_lwf = fields.Boolean(string="Labour Welfare Fund", default=True)
    l10n_in_lwf_employee_contribution = fields.Monetary(related="company_id.l10n_in_lwf_employee_contribution", readonly=False)
    l10n_in_lwf_employer_contribution = fields.Monetary(related="company_id.l10n_in_lwf_employer_contribution", readonly=False)

    l10n_in_basic_salary_percent = fields.Float(related="company_id.l10n_in_basic_salary_percent", readonly=False)
    l10n_in_house_rent_allowance_percent = fields.Float(related="company_id.l10n_in_house_rent_allowance_percent", readonly=False)
    l10n_in_standard_allowance = fields.Float(related="company_id.l10n_in_standard_allowance", readonly=False)
    l10n_in_performance_bonus_percent = fields.Float(related="company_id.l10n_in_performance_bonus_percent", readonly=False)
    l10n_in_leave_travel_allowance_percent = fields.Float(related="company_id.l10n_in_leave_travel_allowance_percent", readonly=False)
    l10n_in_leave_days = fields.Float(related="company_id.l10n_in_leave_days", readonly=False)
    l10n_in_gratuity = fields.Float(related="company_id.l10n_in_gratuity", readonly=False)
    l10n_in_supplementary_allowance = fields.Float(related="company_id.l10n_in_supplementary_allowance", readonly=False)
