from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    _sql_constraints = [
        ('check_epf_employee_contri_positive', 'CHECK(l10n_in_epf_employee_contri >= 0)', "Employee's EPF Contribution cannot be negative."),
        ('check_epf_employer_contri_positive', 'CHECK(l10n_in_epf_employer_contri >= 0)', "Employer's EPF Contribution cannot be negative."),
        ('check_esic_employee_positive', 'CHECK(l10n_in_esic_employee_contri >= 0)', "Employee's ESIC Contribution cannot be negative."),
        ('check_esic_employer_positive', 'CHECK(l10n_in_esic_employer_contri >= 0)', "Employer's ESIC Contribution cannot be negative."),
        ('check_lwf_employee_positive', 'CHECK(l10n_in_lwf_employee_contri >= 0)', "Employee's LWF Contribution cannot be negative."),
        ('check_lwf_employer_positive', 'CHECK(l10n_in_lwf_employer_contri >= 0)', "Employer's LWF Contribution cannot be negative."),
    ]

    l10n_in_org_tax_details = fields.Boolean(string="Organisation Tax Details")
    l10n_in_org_pan_number = fields.Char(string="PAN Number")
    l10n_in_org_tan_number = fields.Char(string="TAN Number")
    l10n_in_org_tds_circle_number = fields.Char(string="TDS Circle/AO Code")

    l10n_in_epf = fields.Boolean(string="Employees' Provident Fund")
    l10n_in_epf_employer_id = fields.Char(string="Employer Identification")
    l10n_in_epf_employee_contri = fields.Float(string="Employee Contribution", default=0.12)
    l10n_in_epf_employer_contri = fields.Float(string="Employer Contribution", default=0.12)

    l10n_in_esic = fields.Boolean(string="Employee's State Insurance Corporation")
    l10n_in_esic_ip_number = fields.Char(string="ESIC IP")
    l10n_in_esic_employee_contri = fields.Float(default=0.0075)
    l10n_in_esic_employer_contri = fields.Float(default=0.0325)

    l10n_in_prof_tax = fields.Boolean(string="Professional Tax")
    l10n_in_prof_tax_number = fields.Char(string="Professional Tax Number")

    l10n_in_lwf = fields.Boolean(string="Labour Welfare Fund")
    l10n_in_lwf_employee_contri = fields.Monetary(string="Employee's Contribution", default=6.00)
    l10n_in_lwf_employer_contri = fields.Monetary(string="Employer's Contribution", default=12.00)
