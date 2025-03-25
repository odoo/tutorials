# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class ProductWarrantyWizardLine(models.TransientModel):
    _name = "product.warranty.wizard.line"
    _description = "product warranty wizard line"

    warranty_wizard_id = fields.Many2one("product.warranty.wizard")
    order_line_id = fields.Many2one("sale.order.line", store=True)
    product_id = fields.Many2one("product.product", store=True)
    linked_product_name = fields.Char(related="product_id.display_name", string="Product Name")
    warranty_product_id = fields.Many2one("product.warranty", string="Year", domain="[('product_id', '=', product_id)]")
    warranty_end_date = fields.Date(readonly=True, compute="_compute_warranty_end_date")

    @api.depends("warranty_product_id")
    def _compute_warranty_end_date(self):
        for record in self:
            record.warranty_end_date = (
                fields.Date.add(fields.Date.today(), years=record.warranty_product_id.year)
                if record.warranty_product_id
                else False
            )
