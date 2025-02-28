from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_unique_id = fields.Char("Unique ID", unique=True)
    import_histry_ids = fields.One2many('product.product','product_id',string="Import Histry")
