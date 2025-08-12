from odoo import fields, models


class ModuleTypes(models.Model):
    _name = "module.types"
    _description = "Module Types"

    name = fields.Char("Module type name", required=True)
    value = fields.Integer("Module type value", default=0)
