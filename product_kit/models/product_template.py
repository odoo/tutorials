from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    kit = fields.Boolean(string="has kit ?", default=False, help="To enable new product type")
    subproduct = fields.Many2many(comodel_name="product.product", string="Sub Product", help="Select subproduct if kit is enabled")
