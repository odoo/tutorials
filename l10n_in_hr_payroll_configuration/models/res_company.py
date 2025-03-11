from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_in_pf_employer_identification = fields.Char(string="Employer Identification")
    l10n_in_esic_ip = fields.Char(string="ESIC IP")
    l10n_in_pt_number = fields.Char(string="Professional Tax Number")
    l10n_in_organization_tax_details = fields.Boolean(string="Organization Tax Details")
    l10n_in_tan_number = fields.Char(string="TAN Number")
    l10n_in_pan_number = fields.Char(string="PAN Number")
    l10n_in_tds_circle = fields.Char(string="TDS Cirle / AO code")
