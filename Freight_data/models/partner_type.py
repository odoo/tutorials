from odoo import models, fields

class PartnerType(models.Model):
    _name = 'partner.type'
    _description = 'Partner Type'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    status = fields.Boolean(string='Status', default=True)
