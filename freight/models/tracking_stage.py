from odoo import models, fields


class TrackingStage(models.Model):
    _name = "tracking.stage"
    _description = "this is tracking stage"

    code = fields.Char(string="Code")
    name = fields.Char(string="Name")
    status = fields.Boolean(string='Status', default=True)
