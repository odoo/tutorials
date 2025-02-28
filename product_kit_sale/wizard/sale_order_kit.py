# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, _, api, fields, models


class SaleOrderKit(models.TransientModel):
    _name = "sale.order.kit"
    _description = "Kit Wizard"

    order_line_id = fields.Many2one(comodel_name="sale.order.line", required=True, ondelete="cascade")
    wizard_line_ids = fields.One2many(comodel_name="sale.order.kit.line", inverse_name="wizard_id")
    should_update = fields.Boolean(help="Whether to update sales order lines or create new ones")

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        order_line_id = self.env.context.get("active_id")
        order_line = self.env["sale.order.line"].browse(order_line_id)
        wizard_lines = []
        should_update = False
        if order_line.sub_product_line_ids:
            should_update = True
            for line in order_line.sub_product_line_ids:
                wizard_lines.append({
                    "product_id": line.product_id.id,
                    "price_unit": line.sub_product_effective_price,
                    "quantity": line.product_uom_qty
                })
        else:
            sub_products = order_line.product_id.sub_product_ids
            for sub_product in sub_products:
                wizard_lines.append({"product_id": sub_product.id})
        res["wizard_line_ids"] = [Command.clear()] + [Command.create(vals) for vals in wizard_lines]
        res["order_line_id"] = order_line_id
        res["should_update"] = should_update
        return res

    def _update_order(self):
        wizard_lines_map = {line.product_id.id: line for line in self.wizard_line_ids}
        total_price = 0
        for order_line in self.order_line_id.sub_product_line_ids:
            wizard_line = wizard_lines_map.get(order_line.product_id.id)
            total_price += wizard_line.price_unit * wizard_line.quantity
            order_line.update({
                'sub_product_effective_price': wizard_line.price_unit,
                'product_uom_qty': wizard_line.quantity,
                'price_unit': 0
            })
        self.order_line_id.update({'price_unit': total_price})

    def action_add_kit_products(self):
        if self.should_update:
            self._update_order()
            return
        vals_list = []
        total_price = 0
        for wizard_line in self.wizard_line_ids:
            total_price += wizard_line.price_unit * wizard_line.quantity
            vals_list.append({
                'order_id': self.order_line_id.order_id.id,
                'product_id': wizard_line.product_id.id,
                'sub_product_effective_price': wizard_line.price_unit,
                'product_uom_qty': wizard_line.quantity,
                'parent_kit_line_id': self.order_line_id.id,
                'price_unit': 0,
                "linked_line_id": self.order_line_id.id
            })
        if len(vals_list) > 0:
            self.env['sale.order.line'].create(vals_list)
        self.order_line_id.update({'total_price': total_price})
