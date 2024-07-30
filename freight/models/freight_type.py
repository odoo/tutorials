from odoo import models, fields


class TransportType(models.Model):
    _name = "freight.type"
    _description = "this is freight type"

    code = fields.Char(string="Code")
    name = fields.Char(string="Name")
    status = fields.Boolean(string='Status', default=True)
