from odoo import fields, models


class TrackingStages(models.Model):
    _name = 'tracking.stages'
    _description = 'Tracking Stages Model'
    _inherits = {'port.city': 'freight_type_id'}

    freight_type_id = fields.Many2one('port.city')
