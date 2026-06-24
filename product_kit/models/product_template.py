from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_kit = fields.Boolean(
        string="Is a Kit",
        help="Check if this product is a kit composed of multiple products.",
    )
    kit_product_ids = fields.One2many(
        'product.kit.line',
        'product_tmpl_id',
        string="Kit Products",
        help="Products that make up this kit.",
    )
