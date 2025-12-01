# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CatalogLines(models.Model):
    _name = 'catalog.lines'
    _description = "Catalog Lines"

    catalog_line_id = fields.Many2one(comodel_name='catalog.catalog')
    product_category_id = fields.Many2one(comodel_name='product.category', string="Product Category")
    color1 = fields.Char(string="Color 1")
    color2 = fields.Char(string="Color 2")
    removed_product_ids = fields.Many2many(comodel_name='product.product')
