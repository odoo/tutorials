from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_kit = fields.Boolean(string='Is Kit')
    sub_product_ids = fields.Many2many(
        'product.product',
        'product_kit_sub_products_rel',
        'kit_id',
        'sub_product_id',
        string='Sub Products',
        domain="[('type', '=', 'product')]"
    )
    show_subproducts_on_report = fields.Boolean(string='Print Subproducts on Report')
