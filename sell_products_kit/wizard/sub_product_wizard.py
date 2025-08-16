from odoo import fields, models, api, Command


class SubProductWizard(models.TransientModel):
    _name = "sub.product.wizard"
    _description = "Sub Product Wizard"

    sale_order_line_id = fields.Many2one("sale.order.line", required=True)
    sub_product_ids = fields.One2many(
        "sub.product.line.wizard", inverse_name="parent_wizard"
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        sale_order_line_id = self._context.get("active_id")
        if sale_order_line_id:
            sale_order_line = self.env["sale.order.line"].browse(sale_order_line_id)
            line_values = []
            existing_lines = self.env["sale.order.line"].search(
                [("parent_line_id", "=", sale_order_line_id)]
            )

            line_values = []
            if existing_lines:
                for sub_product in existing_lines:
                    curr_product = self.env["sub.product.line.wizard"].create(
                        {
                            "product_id": sub_product.product_id.id,
                            "price": sub_product.last_price or sub_product.price_unit,
                            "quantity": sub_product.product_uom_qty,
                        }
                    )
                    line_values.append(Command.link(curr_product.id))
            else:
                for sub_product in sale_order_line.product_id.sub_product_ids:
                    curr_product = self.env["sub.product.line.wizard"].create(
                        {
                            "product_id": sub_product.id,
                            "price": sub_product.list_price,
                            "quantity": 1,
                        }
                    )
                    line_values.append(Command.link(curr_product.id))
            res["sub_product_ids"] = line_values
            res["sale_order_line_id"] = sale_order_line_id
        return res

    def action_confirm(self):
        total_price = 0
        for line in self.sub_product_ids:
            existing_line = self.env["sale.order.line"].search(
                [
                    ("parent_line_id", "=", self.sale_order_line_id.id),
                    ("product_id", "=", line.product_id.id),
                    ("order_id", "=", self.sale_order_line_id.order_id.id),
                ],
                limit=1,
            )

            if existing_line:
                existing_line.product_uom_qty = line.quantity
                existing_line.last_price = line.price
                existing_line.price_unit = 0
            else:
                self.env["sale.order.line"].create(
                    {
                        "order_id": self.sale_order_line_id.order_id.id,
                        "product_id": line.product_id.id,
                        "product_uom_qty": line.quantity,
                        "last_price": line.price,
                        "price_unit": 0,
                        "parent_line_id": self.sale_order_line_id.id,
                    }
                )

            total_price += line.quantity * line.price
        # Update the total price of the parent sale order line
        total_price += (
            self.sale_order_line_id.product_uom_qty
            * self.sale_order_line_id.product_template_id.list_price
        )
        self.sale_order_line_id.price_unit = total_price
        return True
