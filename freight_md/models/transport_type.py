from odoo import fields, models


class TransportType(models.Model):
    _name = 'transport.type'
    _description = 'Transport Type'

    code = fields.Char('Code', required=True)
    name = fields.Char('Name', required=True)
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string='Status', default='active')
