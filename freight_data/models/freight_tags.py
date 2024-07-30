from odoo import fields, models


class FreightTags(models.Model):
    _name = 'freight.tags'
    _description = 'Freight Tags'
    _inherits = {'port.city': 'freight_type_id'}

    freight_type_id = fields.Many2one('port.city')
