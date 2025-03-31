# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'
     
    is_warranty_available = fields.Boolean(string="Is Warranty Available")
