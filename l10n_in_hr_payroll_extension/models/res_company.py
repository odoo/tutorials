from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    l10n_in_org_tax_details = fields.Boolean(string="Organisation Tax Details")
    l10n_in_org_pan_number = fields.Char(string="PAN Number")
    l10n_in_org_tan_number = fields.Char(string="TAN Number")
    l10n_in_org_tds_circle = fields.Char(string="TDS Circle/AO Code")

    l10n_in_employer_identification = fields.Char(string="Employer Identification")
    l10n_in_professional_tax_number = fields.Char(string="Professional Tax Number")
    l10n_in_esic_ip = fields.Char(string="ESIC IP")
