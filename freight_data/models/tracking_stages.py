from odoo import models, fields


class TrackingStages(models.Model):
    _name = 'tracking.stages'
    _description = 'Freight Service Tracking Stages'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    status = fields.Boolean(string='Status', default=True)
