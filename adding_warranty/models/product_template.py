# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class product_template(models.Model):
    _inherit = "product.template"

    is_warranty_available = fields.Boolean(string="Is Warranty Available")
    warranty_id = fields.Many2one("warranty.configuration",string="Select Warranty")
