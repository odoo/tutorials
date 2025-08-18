from odoo import api, fields, models


class SubProductsWizard(models.TransientModel):
    _name = "sub.products.wizard"
    _description = "Wizard to Configure Kit Sub-Products"

    order_line_id = fields.Many2one(
        "sale.order.line",
        string="Sale Order Line",
        required=True,
        readonly=True,
        help="The main sale order line for the kit product.",
    )
    order_id = fields.Many2one(
        related="order_line_id.order_id",
        string="Sale Order",
    )
    product_id = fields.Many2one(
        related="order_line_id.product_id",
        string="Kit Product",
    )

    sub_product_line_ids = fields.One2many(
        "sub.products.line.wizard",
        "sub_products_wizard_id",
        string="Sub-Products",
    )

    total_price = fields.Float(
        string="Total Kit Price",
        compute="_compute_total_price",
        digits="Product Price",
        help="The final price of the main kit product based on the components.",
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if self.env.context.get("active_id"):
            order_line = self.env["sale.order.line"].browse(
                self.env.context.get("active_id")
            )
            res["order_line_id"] = order_line.id

            default_sub_products = order_line.product_id.sub_products

            existing_sub_lines_map = {
                line.product_id: line for line in order_line.sub_product_line_ids
            }

            wizard_lines = []
            for sub_product in default_sub_products:
                existing_line = existing_sub_lines_map.get(sub_product)
                if existing_line:
                    quantity = existing_line.product_uom_qty
                    price = (
                        existing_line.price_unit
                        if existing_line.price_unit > 0
                        else sub_product.lst_price
                    )
                else:
                    quantity = 1.0
                    price = sub_product.lst_price

                wizard_lines.append(
                    (
                        0,
                        0,
                        {
                            "product_id": sub_product.id,
                            "quantity": quantity,
                            "price": price,
                        },
                    )
                )

            res["sub_product_line_ids"] = wizard_lines
        return res

    def action_confirm(self):
        self.ensure_one()

        self.order_line_id.sub_product_line_ids.unlink()

        new_lines_vals = []
        for line in self.sub_product_line_ids:
            new_lines_vals.append(
                {
                    "order_id": self.order_id.id,
                    "product_id": line.product_id.id,
                    "product_uom_qty": line.quantity,
                    "price_unit": 0, 
                    "parent_kit_line_id": self.order_line_id.id,
                    "is_kit_sub_product": True,
                }
            )
        self.env["sale.order.line"].create(new_lines_vals)

        self.order_line_id.price_unit = self.total_price

        return {"type": "ir.actions.act_window_close"}

    @api.depends("sub_product_line_ids.quantity", "sub_product_line_ids.price")
    def _compute_total_price(self):
        for wizard in self:
            wizard.total_price = sum(
                line.quantity * line.price for line in wizard.sub_product_line_ids
            )
