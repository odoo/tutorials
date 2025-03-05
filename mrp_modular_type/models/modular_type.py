from odoo import fields, models

class ModularType(models.Model):
    _name = 'modular.type'

    name = fields.Char(string="Modular Type Name")
