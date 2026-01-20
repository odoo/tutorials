from odoo import models, fields, api


class SubProductWizard(models.TransientModel):
    _name = "sale.sub.product.wizard"
    _description = "Select Sub Products"

    sale_order_id = fields.Many2one("sale.order", string="Sale Order", readonly=True)

    sub_product_wizard_line_ids = fields.One2many(
        "sale.sub.product.wizard.line", "sub_product_wizard_id"
    )
    sub_product_ids = fields.Many2many(
        "product.product", string="Sub Products", readonly=True
    )
    main_line_id = fields.Many2one(
        "sale.order.line", string="Main Kit Line", readonly=True
    )
    cost = fields.Float(string="Total Cost", compute="_compute_total_cost")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get("active_id")

        line = self.env["sale.order.line"].browse(active_id)

        sub_products = line.product_id.product_tmpl_id.sub_products_ids

        sub_products_lines = []

        prev_sub_prod = line.order_id.order_line.filtered(
            lambda ln: ln.parent_kit_id.id == line.id
        )

        def add_sub_product_line(data):
            sub_products_lines.append((0, 0, data))

        if prev_sub_prod and len(prev_sub_prod) == len(sub_products):
            for product, prev_prod in zip(sub_products, prev_sub_prod):
                add_sub_product_line(
                    {
                        "product_id": product.id,
                        "price": product.list_price,
                        "quantity": prev_prod.product_uom_qty,
                    }
                )
        else:
            for product in sub_products:
                add_sub_product_line(
                    {
                        "product_id": product.id,
                        "price": product.list_price,
                    }
                )

        res.update(
            {
                "main_line_id": line.id,
                "sale_order_id": line.order_id.id,
                "sub_product_wizard_line_ids": sub_products_lines,
                "sub_product_ids": [(6, 0, sub_products.ids)],
            }
        )
        return res

    def action_add_sub_products(self):
        for line, sub_product in zip(
            self.sub_product_wizard_line_ids, self.sub_product_ids
        ):
            exisating_lines = self.sale_order_id.order_line.filtered(
                lambda ln: ln.product_id.id == sub_product.id
                and ln.parent_kit_id.id == self.main_line_id.id
            )

            if exisating_lines:
                exisating_lines.write(
                    {
                        "product_uom_qty": line.quantity,
                        "price_unit": 0.0,
                    }
                )
            else:
                self.env["sale.order.line"].create(
                    {
                        "order_id": self.sale_order_id.id,
                        "product_id": sub_product.id,
                        "product_uom_qty": line.quantity,
                        "price_unit": 0.0,
                        "parent_kit_id": self.main_line_id.id,
                    }
                )

        main_prod_cost = self.main_line_id.original_price_unit + self.cost
        self.main_line_id.write({"price_unit": main_prod_cost})

        return {"type": "ir.actions.act_window_close"}

    @api.depends("sub_product_wizard_line_ids.quantity")
    def _compute_total_cost(self):
        for wizard in self:
            total_cost = sum(
                (line.price * line.quantity)
                for line in wizard.sub_product_wizard_line_ids
            )
            wizard.cost = total_cost
