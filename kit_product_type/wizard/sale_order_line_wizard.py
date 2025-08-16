from odoo import api, fields, models


class SubProducts(models.TransientModel):
    _name = "sale.order.line.wizard"
    _description = "change.quantity.of.subproducts.in.kit"

    main_product_id = fields.Many2one('sale.order.line', string="Main Order Line", readonly=True)

    line_ids = fields.One2many(
        "sale.order.line.wizard.line", "wizard_id", string="Sub Products"
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get("active_id")
        main_order_line = self.env["sale.order.line"].browse(active_id)
        sale_order = main_order_line.order_id
        order_line = self.env["sale.order.line"].browse(active_id)
        res["main_product_id"] = main_order_line.id

        if order_line:
            lines = []
            for product in order_line.product_template_id.sub_products:
                existing_line = self.env["sale.order.line"].search(
                    [
                        ("order_id", "=", sale_order.id),
                        ("main_order_line_id", "=", main_order_line.id),
                        ("product_id", "=", product.id),
                    ],
                    limit=1,
                )
                lines.append(
                    (
                        0,
                        0,
                        {
                            "product_id": product.id,
                            "quantity": existing_line.product_uom_qty if existing_line else 1,
                            "price": existing_line.price_unit if existing_line else product.list_price,
                        },
                    )
                )
            res["line_ids"] = lines
        return res

    def confirm_sub_products(self):
        active_id = self.env.context.get("active_id")
        main_order_line = self.env["sale.order.line"].browse(active_id)
        sale_order = main_order_line.order_id
        main_product_subtotal = (
            main_order_line.price_unit * main_order_line.product_uom_qty
        )
        for wizard in self:
            for line in wizard.line_ids:
                if line.quantity > 0:
                    main_product_subtotal += line.quantity * line.price

                    existing_line = self.env["sale.order.line"].search(
                        [
                            ("order_id", "=", sale_order.id),
                            ("main_order_line_id", "=", main_order_line.id),
                            ("product_id", "=", line.product_id.id),
                        ],
                        limit=1,
                    )

                    if existing_line:
                        existing_line.write(
                            {
                                "product_uom_qty": line.quantity,
                                "price_unit": line.price,
                            }
                        )
                    else:
                        self.env["sale.order.line"].create(
                            {
                                "order_id": sale_order.id,
                                "product_id": line.product_id.id,
                                "product_uom_qty": line.quantity,
                                "name": line.product_id.name,
                                "is_sub_product_ol": True,
                                "price_unit": line.price,
                                "main_order_line_id": main_order_line.id,
                            }
                        )
        main_order_line.write({"price_subtotal": main_product_subtotal})
