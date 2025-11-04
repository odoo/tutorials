from odoo import fields, models


class ProductModularType(models.Model):
    _name = 'product.modular.type'
    _description = 'Modular Types for Products'

    name = fields.Char(string='Name', required=True)
