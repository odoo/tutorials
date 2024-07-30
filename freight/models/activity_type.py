from odoo import models, fields


class ActivityType(models.Model):
    _name = "activity.type"
    _description = "this is Activity Type"

    code = fields.Char(string="Code")
    name = fields.Char(string="Name")
    status = fields.Boolean(string='Status', default=True)
