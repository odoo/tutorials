from odoo import fields, models


class TrakingType(models.Model):
    _name = 'traking.type'
    _description = 'Traking Type Model'
    _inherits = {'freight.data': 'freight_type_id'}

    freight_type_id = fields.Many2one('freight.data')
