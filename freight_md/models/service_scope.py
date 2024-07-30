from odoo import models, fields


class ServiceScope(models.Model):
    _name = 'service.scope'
    _description = 'Service Scope'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    status = fields.Boolean(string='Status', default=True)
