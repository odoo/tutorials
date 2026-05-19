from odoo import fields, models


class ModularType(models.Model):
    _name = 'modular.type'
    _description = 'Modular Types'

    name = fields.Char()
