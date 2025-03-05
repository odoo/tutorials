# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    _description = "Sales Order Line"

    order_line_linked_to_warranty = fields.Many2one(comodel_name="sale.order.line", copy=False , string="Warranty Product", ondelete="cascade")
    has_warranty = fields.Boolean(string="Is Warranty Added", copy=False)
    is_warranty = fields.Boolean(string="Is warranty")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals['is_warranty'] and vals.get('order_line_linked_to_warranty') is None:
                vals_list.remove(vals)
        return super().create(vals_list)

    @api.ondelete(at_uninstall=False)
    def _unlink_except_confirmed(self):
        super()._unlink_except_confirmed()
        for line in self:
            if line.is_warranty: 
                line.order_line_linked_to_warranty.write({'has_warranty': False})
