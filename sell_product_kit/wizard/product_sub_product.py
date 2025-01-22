
from odoo import _, fields, models

class ProductSubProduct(models.TransientModel):
    _name = 'product.sub.product'
    _description="Wizard to add sub products in a product"
    
    sub_products= fields.Many2many(string="Product", comodel_name="product.product")
    quantity= fields.Float(string="Quantity")
    price= fields.Float(string="Price")
    

    
