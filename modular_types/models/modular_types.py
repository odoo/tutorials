from odoo import fields, models


class ModularTypes(models.Model):
    _name = "modular.types"
    _description = 'Modular types with multiplier value'

    name = fields.Char(string="Modular Types")
    multiplier = fields.Integer(string="Value")
