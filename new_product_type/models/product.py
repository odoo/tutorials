from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_kit = fields.Boolean(string="Is Kit", help="Check if this product is sold as a kit")
    kit_product_ids = fields.Many2many(
        'product.product', 
        string="Sub Products", 
        help="Select products that are part of this kit"
    )
