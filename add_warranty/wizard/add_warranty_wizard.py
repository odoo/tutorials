# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class AddWarrantyLinesWizard(models.TransientModel):
    _name = "add.warranty.lines.wizard"
    _description = "Add Warranty Lines Wizard"

    wizard_id = fields.Many2one('add.warranty.wizard', string="Wizard Reference", ondelete="cascade")
    product_id = fields.Many2one(comodel_name="product.product", string="Product")
    sale_order_line_id = fields.Many2one(comodel_name="sale.order.line", string="Sale order lines")
    year_id = fields.Many2one(comodel_name="warranty.config", string="Year")
    end_date = fields.Date(readonly=True, string="End Date", compute="_compute_end_date")

    @api.depends('year_id')
    def _compute_end_date(self):
        for record in self:
            record.end_date = record.year_id and fields.Date.today() + relativedelta(days=365 * record.year_id.period) or False

class AddWarrantyWizard(models.TransientModel):
    _name = "add.warranty.wizard"
    _description = "Add Warranty Wizard"

    wizard_line_ids = fields.One2many(comodel_name='add.warranty.lines.wizard', inverse_name='wizard_id', string="Products")

    def default_get(self,fields_list):
        res = super().default_get(fields_list)
        sale_order = self.env['sale.order'].browse(self.env.context.get("default_sale_order_id"))
        sale_order_lines = sale_order.order_line.filtered(lambda line: line.product_id.warranty_available and not line.has_warranty)
        res.update({
            'wizard_line_ids': [(0,0, {
            'sale_order_line_id' : line.id,
            'product_id': line.product_id.id
            }) for line in sale_order_lines]
        })
        return res

    def action_add(self):
        sale_order_line = self.env['sale.order.line']
        warranty_lines = self.wizard_line_ids
        for line in warranty_lines:
            if line.year_id:
                sale_order_line.create({
                    'order_id': line.sale_order_line_id.order_id.id,
                    'product_id':  line.year_id.product.id,
                    'product_uom_qty': 1,
                    'price_unit': line.year_id.percentage / 100 * line.sale_order_line_id.price_unit,
                    'name': f"{line.sale_order_line_id.product_id.name} Warranty, End Date: {line.end_date}",
                    'order_line_linked_to_warranty': line.sale_order_line_id.id,
                    'is_warranty': True,
                })
                line.sale_order_line_id.write({'has_warranty': True})
        return True
