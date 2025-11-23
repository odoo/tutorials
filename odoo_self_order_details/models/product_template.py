# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    self_order_description = fields.Html(string="Self order description",   translate=True)
