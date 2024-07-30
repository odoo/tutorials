from odoo import models, fields


class FreightTags(models.Model):
    _name = 'freight.tags'
    _description = 'Freight Tags'
    _inherits = {'freight.data': 'freight_type_id'}

    freight_type_id = fields.Many2one('freight.data')
