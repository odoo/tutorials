from odoo import fields, models


class LadingType(models.Model):
    _name = 'lading.type'
    _description = 'Lading Type Model'
    _inherits = {'freight.data': 'freight_type_id'}

    freight_type_id = fields.Many2one('freight.data')
