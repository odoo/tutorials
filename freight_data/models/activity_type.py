from odoo import fields, models


class ActivityType(models.Model):
    _name = 'activity.type'
    _description = 'Activity Type Model'
    _inherits = {'freight.data': 'freight_type_id'}

    freight_type_id = fields.Many2one('freight.data')
