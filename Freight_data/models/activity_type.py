from odoo import models, fields

class ActivityType(models.Model):
    _name = 'activity.type'
    _description = 'Activity Type'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    status = fields.Boolean(string='Status', default=True)
