from odoo import fields, models


class PaartnerType(models.Model):
    _name = 'partner.type'
    _description = 'Partner Type Model'
    _inherits = {'freight.data': 'freight_type_id'}

    freight_type_id = fields.Many2one('freight.data')
