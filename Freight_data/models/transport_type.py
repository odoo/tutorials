from odoo import models, fields, api

class TransportType(models.Model):
    _name = 'transport.type'
    _description = 'Transport'

    code = fields.Char(string="Code")
    name = fields.Char(string="Name")
    active = fields.Boolean(string="Active", default=True)
