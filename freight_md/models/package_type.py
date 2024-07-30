from odoo import fields, models


class PackageType(models.Model):
    _name = 'package.type'
    _description = 'Package Type'

    code = fields.Char('Code', required=True)
    name = fields.Char('Name', required=True)
    is_lcl = fields.Boolean('LCL')
    is_air = fields.Boolean('AIR')
    status = fields.Boolean('Active', default=True)
