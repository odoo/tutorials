# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from odoo.tools.translate import html_translate


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    wbsp_product_description = fields.Html(
        string='Ecommerce Extended Description', translate=html_translate)
