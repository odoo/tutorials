from odoo import fields, models


class PackageSelection(models.Model):
    _name = 'package.selection'
    _description = 'Package Selection Options'

    name = fields.Char(required=True, string="Package Selection")
