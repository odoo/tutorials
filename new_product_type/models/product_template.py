# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_kit = fields.Boolean(string="Is Kit")
    sub_products = fields.Many2many(string="Sub Products", comodel_name="product.product", domain="[('is_kit', '=', False)]")
