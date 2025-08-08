# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class SaleOrderLineWizard(models.TransientModel):
    _name = "sale.order.line.wizard"
    _description = "Distribute Price Wizard"

    line_ids = fields.One2many("sale.order.line.wizard.line", "wizard_id", string="Sale Order Lines")

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        active_line_id = self._context.get("active_id")
        active_line = self.env["sale.order.line"].browse(active_line_id)
        order = active_line.order_id
        lines_to_divide = order.order_line.filtered(
            lambda line: line.id != active_line.id
        )
        lines = []
        for line in lines_to_divide:
            line = self.env["sale.order.line.wizard.line"].create(
                {
                    "wizard_id": self.id,
                    "product_id": line.product_id.id,
                    "sale_order_line_id": line.id,
                    "divided_price": active_line.price_subtotal / len(lines_to_divide) if lines_to_divide else 0,
                }
            )
            lines.append(line.id)
            res["line_ids"] = [(6, 0, lines)]
        return res

    def action_divide(self):
        active_line_id = self._context.get("active_id")
        source_sale_order_line_id = self.env["sale.order.line"].browse(active_line_id)
        current_total_price = source_sale_order_line_id.price_subtotal
        sum_price = 0
        for line in self.line_ids:
            sum_price += line.divided_price
        if sum_price > current_total_price:
            raise UserError(_('Sum of divided prices cannot be more than the total price of the source sale order line.'))
        else:
            if sum_price < (source_sale_order_line_id.price_subtotal - source_sale_order_line_id.distributed_price):
                source_sale_order_line_id.price_subtotal -= sum_price
            else:
                source_sale_order_line_id.price_subtotal -= sum_price
                source_sale_order_line_id.distributed_price = source_sale_order_line_id.price_subtotal
        for line in self.line_ids:
            if line.divided_price < 0:
                raise UserError(_('Divided price cannot be negative.'))

            target_sale_order_line = line.sale_order_line_id

            self.env['sale.order.line.distribution'].create({
                'source_sale_order_line_id': source_sale_order_line_id.id,
                'target_sale_order_line_id': target_sale_order_line.id,
                'price': line.divided_price,
            })

            target_sale_order_line.write({
                'distributed_price': target_sale_order_line.distributed_price + line.divided_price,
                'price_subtotal': target_sale_order_line.price_subtotal + line.divided_price
            })  

class SaleOrderLineWizardLine(models.TransientModel):
    _transient_max_count = 0
    _name = "sale.order.line.wizard.line"
    _description = "Distribute Price Wizard Lines"

    wizard_id = fields.Many2one("sale.order.line.wizard", string="Wizard")
    sale_order_line_id = fields.Many2one("sale.order.line", string="Sale Order Line")
    product_id = fields.Many2one("product.product", string="Product")
    divided_price = fields.Float(string="Divided Price")
    include_for_division = fields.Boolean(string="Include for Division", default=True)

    @api.onchange('include_for_division')
    def _onchange_divided_price(self):
        active_line_id = self._context.get("active_id")
        active_line = self.env["sale.order.line"].browse(active_line_id)
        current_total_price = active_line.price_subtotal

        selected_lines = self.wizard_id.line_ids.filtered(lambda line: line.include_for_division)

        for line in self.wizard_id.line_ids:
            if line.include_for_division:
                line.divided_price = current_total_price / len(selected_lines)
            else:
                line.divided_price = 0
