# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    warranty = fields.Boolean(string="Warranty", help="Is warranty available for this product?")
