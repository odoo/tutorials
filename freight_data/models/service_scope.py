from odoo import fields, models


class ServiceScope(models.Model):
    _name = 'service.scope'
    _description = 'Service Scope Model'
    _inherits = {'port.city': 'freight_type_id'}

    freight_type_id = fields.Many2one('port.city')
    description = fields.Text(string='Description')