from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    l10n_in_org_tax_details = fields.Boolean(string="Organisation Tax Details")
    l10n_in_org_pan_number = fields.Char(string="PAN Number")
    l10n_in_org_tan_number = fields.Char(string="TAN Number")
    l10n_in_org_tds_circle = fields.Char(string="TDS Circle/AO Code")

    l10n_in_pf_employer_identification = fields.Char(string="Employer Identification")
    l10n_in_pf_employee_contribution = fields.Float(string="Employee Contribution", default=12)
    l10n_in_pf_employer_contribution = fields.Float(string="Employer Contribution", default=12)

    l10n_in_professional_tax_number = fields.Char(string="Professional Tax Number")

    l10n_in_esic_ip = fields.Char(string="ESIC IP")
    l10n_in_esic_employee_contribution = fields.Float(string="Employee Contribution", default=0.75)
    l10n_in_esic_employer_contribution = fields.Float(string="Employer Contribution", default=3.25)

    l10n_in_lwf_employee_contribution = fields.Monetary(string="Employee Contribution", currency_field="currency_id", default=6)
    l10n_in_lwf_employer_contribution = fields.Monetary(string="Employer Contribution", currency_field="currency_id", default=12)

    # Salary Structure
    l10n_in_basic_salary_percent = fields.Float(string="Basic Salary Percentage", default=0.50)
    l10n_in_house_rent_allowance_percent = fields.Float(string="House Rent Allowance", help="You can define 50% for metro city and 40% for non-metro city.", default=0.50)
    l10n_in_standard_allowance = fields.Float(string="Standard Allowance", default=4167)
    l10n_in_performance_bonus_percent = fields.Float(string="Performance Bonus", default=0.20)
    l10n_in_leave_travel_allowance_percent = fields.Float(string="Leave Travel Allowance", default=0.20)
    l10n_in_leave_days = fields.Float(string="Leave Days", default=1)
    l10n_in_gratuity = fields.Float(string="Gratuity")
    l10n_in_supplementary_allowance = fields.Float(string="Supplementary Allowance")
