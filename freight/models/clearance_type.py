from odoo import models, fields


class ClearanceType(models.Model):
    _name = "clearance.type"
    _description = "this is Clearance type"

    code = fields.Char(string="Code")
    name = fields.Char(string="Name")
    status = fields.Boolean(string='Status', default=True)
