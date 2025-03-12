from odoo import fields, models


class ModuleTypes(models.Model):
    _name = "module.types"
    _description = "Modular Types"

    name = fields.Char(string="Module name")
