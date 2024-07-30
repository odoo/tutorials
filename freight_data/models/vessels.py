from odoo import fields, models


class Vessels(models.Model):
    _name = 'vessels'
    _description = 'vessels Model'
    _inherits = {'port.city': 'freight_type_id'}

    freight_type_id = fields.Many2one('port.city')
    vessel_owner = fields.Many2one('res.partner', string='Vessel Owner')