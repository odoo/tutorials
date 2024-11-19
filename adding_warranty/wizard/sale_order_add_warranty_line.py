# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrderAddWarrantyLine(models.TransientModel):
     _name = "sale.order.add.warranty.line"
     _description = "Warranty Selection"

     wizard_id = fields.Many2one("sale.order.add.warranty", required=True, ondelete="cascade")
     sale_order_line_id = fields.Many2one("sale.order.line", required=True, ondelete="cascade")
     product_id = fields.Many2one("product.product")
     warranty_id = fields.Many2one("warranty.configuration", string="Warranty Years")
     end_date = fields.Date(string="End Date", compute="_compute_end_date")

     @api.depends("warranty_id")
     def _compute_end_date(self):
         for record in self:
             if record.warranty_id:
                 record.end_date = fields.Date.add(fields.Date.today(), years=record.warranty_id.period)
             else:
                 record.end_date = False
