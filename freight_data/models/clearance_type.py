from odoo import models, fields


class ClearanceType(models.Model):
    _name = "clearance.type"
    _description = "Clearance Type"

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    status = fields.Boolean(string='Status', default=True)
