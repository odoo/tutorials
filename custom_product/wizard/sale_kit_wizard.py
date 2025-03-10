from odoo import api, models, fields


class SaleKitWizard(models.TransientModel):
    _name = "sale.kit.wizard"
    _description = "Configure kit Products"

    sale_order_id = fields.Many2one("sale.order", string="Sale order", required=True)
    kit_product_id = fields.Many2one("product.product", string="Product", required=True)
    kit_line_ids = fields.One2many(
        "sale.kit.line.wizard", "wizard_id", string="kit Components"
    )
    kit_parent_id = fields.Many2one("sale.order.line", string="Kit Parent Line")

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        product_id = res['kit_product_id']
        kit_parent_id = self.env.context.get("active_id")
        sale_order_id = self.env.context.get("default_sale_order_id")
        kit_line = []
        if sale_order_id and product_id:
            product = self.env["product.product"].browse(product_id)

            # Look for existing sale order lines related to the current product and kit
            sale_order_lines = self.env["sale.order.line"].search(
                [
                    ("order_id", "=", sale_order_id),
                    ("kit_parent_id", "=", kit_parent_id),
                ]
            )

            for pro in product.product_tmpl_id.kit_product_ids:
                existing_line = sale_order_lines.filtered(
                    lambda line: line.product_id.id == pro.id
                )
                if existing_line:
                    price_unit = existing_line.product_uom_qty * pro.list_price
                    kit_line.append(
                        (
                            0,
                            0,
                            {
                                "product_id": pro.id,
                                "quantity": existing_line.product_uom_qty,
                                "price": price_unit,
                            },
                        )
                    )
                else:
                    kit_line.append(
                        (
                            0,
                            0,
                            {
                                "product_id": pro.id,
                                "quantity": 1,
                                "price": pro.list_price,
                            },
                        )
                    )
            res.update(
                {
                    "kit_parent_id": kit_parent_id,
                    "kit_line_ids": kit_line,
                }
            )
        return res

    def action_confirm_kit(self):
        order = self.sale_order_id
        total_price = 0
        for line in self.kit_line_ids:
            existing_order_line = order.order_line.filtered(
                lambda ln: ln.product_id.id == line.product_id.id
                and ln.kit_parent_id.id == self.kit_parent_id.id
            )

            if existing_order_line:
                existing_order_line.product_uom_qty = line.quantity
                existing_order_line.price_unit = 0.0
            else:
                order.order_line.create(
                    {
                        "order_id": order.id,
                        "product_id": line.product_id.id,
                        "product_uom_qty": line.quantity,
                        "price_unit": 0.0,
                        "kit_parent_id": self.kit_parent_id.id,
                    }
                )
            total_price += line.price * line.quantity

        self.kit_parent_id.price_unit = (
            self.kit_parent_id.product_id.list_price + total_price
        )


class SaleKitLineWizard(models.TransientModel):
    _name = "sale.kit.line.wizard"
    _description = "Kit Product Line"

    wizard_id = fields.Many2one("sale.kit.wizard", string="Wizard", required=True)
    product_id = fields.Many2one("product.product", string="Product")
    quantity = fields.Float(string="Quantity", default=1.0)
    price = fields.Float(string="Price", default=0.0)
