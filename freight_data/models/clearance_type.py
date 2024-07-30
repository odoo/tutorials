from odoo import fields, models


class ClearanceType(models.Model):
    _name = 'clearance.type'
    _description = 'Clearance Type Model'
    _inherits = {'port.city': 'freight_type_id'}

    freight_type_id = fields.Many2one('port.city')
