from odoo import models, fields


class TrackingStage(models.Model):
    _name = 'tracking.stage'
    _description = 'Tracking Stage'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    status = fields.Boolean(string='Status', default=True)
