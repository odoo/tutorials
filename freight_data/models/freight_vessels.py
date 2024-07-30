from odoo import fields, models


class Vessels(models.Model):
    _name = 'freight.vessels'
    _description = 'vessels Model'
    _inherits = {'freight.data': 'freight_type_id'}

    freight_type_id = fields.Many2one('freight.data')
    vessel_owner = fields.Many2one('res.partner', string='Vessel Owner')
