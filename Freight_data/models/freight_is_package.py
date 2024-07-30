from odoo import models, fields

class FreightIsPackage(models.Model):
    _name = 'freight.is.package'
    _description = 'Package Options'

    name = fields.Char(string='Name', required=True)
