from odoo import models, fields, api


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
        kit_parent_id = self.env.context.get("active_id")
        sale_order_id = self.env.context.get("default_sale_order_id")
        product_id = self.env.context.get("default_product_id")
        print("parent_id", kit_parent_id)
        print("order_id", sale_order_id)
        print("product", product_id)

        kit_line = []
        if sale_order_id and product_id:
            product = self.env["product.product"].browse(product_id)
            for pro in product.product_tmpl_id.kit_product_ids:
                print(pro.id)
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
                    "sale_order_id": sale_order_id,
                    "kit_product_id": product_id,
                    "kit_parent_id": kit_parent_id,
                    "kit_line_ids": kit_line,
                }
            )
        return res

    def confirm_kit(self):
        order = self.sale_order_id
        for line in self.kit_line_ids:
            print(self.kit_parent_id)
            order.order_line.create(
                {
                    "order_id": order.id,
                    "product_id": line.product_id.id,
                    "product_uom_qty": line.quantity,
                    "price_unit": line.price,
                    "kit_parent_id": self.kit_parent_id.id,
                }
            )


class SaleKitLineWizard(models.TransientModel):
    _name = "sale.kit.line.wizard"
    _description = "Kit Product Line"

    wizard_id = fields.Many2one("sale.kit.wizard", string="Wizard", required=True)
    product_id = fields.Many2one("product.product", string="Product")
    quantity = fields.Float(string="Quantity", default=1.0)
    price = fields.Float(string="Price", default=0.0)
