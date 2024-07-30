from odoo import fields, models


class ServiceScope(models.Model):
    _name = 'service.scope'
    _description = 'Service Scope Model'
    _inherits = {'freight.data': 'freight_type_id'}

    freight_type_id = fields.Many2one('freight.data')
    description = fields.Text(string='Description')
