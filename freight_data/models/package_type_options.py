from odoo import fields, models


class PackageTypeOptions(models.Model):
    _name = "package.type.options"
    _description = "Package Type Options Model"

    name = fields.Char()
