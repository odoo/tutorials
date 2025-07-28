from odoo import models, fields


class ModularTypeConfig(models.Model):
    _name = 'modular.type.config'
    _description = 'Configuration for Modular Types'

    name = fields.Char(string='Modular Type Name', required=True)
    default_quantity = fields.Float(string='Default Quantity', default=1.0, required=True)
    component_product_id = fields.Many2one(
        'product.product',
        string='Component Product',
        required=True,
        help="The product that represents this modular component on the sales order line."
    )
