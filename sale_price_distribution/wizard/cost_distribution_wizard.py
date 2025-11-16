# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api , fields, models
from odoo.exceptions import UserError

class CostDistributionWizard(models.TransientModel):
    _name = "cost.distribution.wizard"
    _description = "Wizard to distribute cost across other sales order lines."

    order_line_id = fields.Many2one("sale.order.line", string="Order Line")
    order_line_ids = fields.Many2many("sale.order.line", string="Order Lines")
    order_line_cost = fields.Float(string="Cost to Distribute")
    order_id = fields.Many2one("sale.order", string="Sales Order")
    price_subtotal = fields.Float(string="Price Subtotal")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        order_id = self.env.context.get("order_id")
        selected_line_id = self.env.context.get("default_order_line_id")
        total_cost = self.env.context.get("default_price_subtotal", 0)

        if order_id:
            order = self.env["sale.order"].browse(order_id)
            line_ids = order.order_line.ids

            # Remove the selected line from distribution
            if selected_line_id in line_ids:
                line_ids.remove(selected_line_id)

            res.update({
                "order_id": order_id,
                "order_line_ids": [(6, 0, line_ids)],
                "order_line_cost": total_cost,
            })

            # Distribute cost evenly
            per_line_cost = round(total_cost / len(line_ids), 2) if line_ids else 0
            for line in self.env["sale.order.line"].browse(line_ids):
                    line.write({"distributed_cost": per_line_cost})

        return res

    def distribute_cost(self):
        total_distributed = sum(line.distributed_cost for line in self.order_line_ids)

        if total_distributed > self.price_subtotal:
            raise UserError("Total distributed cost exceeds the original amount.")

        # Add distributed cost to each line and update unit price
        for line in self.order_line_ids:
            if line.product_uom_qty > 0:  # Avoid division by zero
                new_unit_price = line.price_unit + (line.distributed_cost / line.product_uom_qty)
                line.write({
                    "price_subtotal": line.price_subtotal + line.distributed_cost,
                    "price_unit": new_unit_price
                })

        # Deduct from the original order line
        original_line = self.env["sale.order.line"].browse(self.env.context.get("default_order_line_id"))
        original_line.write({
            "price_subtotal": original_line.price_subtotal - total_distributed,
            "price_unit": original_line.price_unit - (total_distributed / original_line.product_uom_qty) if original_line.product_uom_qty > 0 else original_line.price_unit
        })

        if original_line.price_unit == 0:
            original_line.unlink()
