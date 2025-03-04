from odoo import api, Command, fields, models


class SubProductsWizard(models.TransientModel):
    _name = "subproducts.wizard"
    _description = "Wizard to select sub products"

    product_id = fields.Many2one("product.product", string="Product", required=True)
    line_ids = fields.One2many(
        "subproducts.wizard.line", "wizard_id", string="Sub Products"
    )
    parent_id = fields.Many2one("sale.order.line", string="Parent Line")

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        product_id = self.env.context.get("default_product_id")
        order_id = self.env.context.get("active_id")
        parent_id = self.env.context.get("default_parent_id")

        if not product_id or not order_id:
            return res

        product = self.env["product.product"].browse(product_id)
        order = self.env["sale.order"].browse(order_id)
        sub_products = product.sub_product_ids
        lines = []

        for sub in sub_products:
            existing_line = order.order_line.filtered(
                lambda l: l.product_id.id == sub.id
                and l.parent_line_id
                and l.parent_line_id.id == parent_id
            )

            lines.append(Command.create({
                        "product_id": sub.id,
                        "quantity": existing_line.product_uom_qty if existing_line else 1.0,
                        "price": existing_line.price_current if existing_line else sub.lst_price,
                    }))

        res.update(
            {
                "product_id": product_id,
                "line_ids": lines,
                "parent_id": parent_id,
            }
        )
        return res

    def action_confirm(self):
        order_id = self.env.context.get("active_id")
        parent_id = self.env.context.get("default_parent_id")

        order = self.env["sale.order"].browse(order_id)
        parent_line = order.order_line.filtered(lambda l: l.id == parent_id)
        total_price = self.product_id.lst_price

        for line in self.line_ids:
            existing_line = order.order_line.filtered(
                lambda l: l.product_id.id == line.product_id.id
                and l.parent_line_id
                and l.parent_line_id.id == parent_id
            )
            if existing_line:
                existing_line.write({
                    'product_uom_qty': line.quantity,
                    'price_current': line.price,
                    'price_unit': 0,
                })

            else:
                self.env["sale.order.line"].create(
                    {
                        "order_id": order.id,
                        "product_id": line.product_id.id,
                        "product_uom_qty": line.quantity,
                        "price_current": line.price,
                        "price_unit": 0,
                        "name": line.product_id.name,
                        "is_subproduct": True,
                        "sequence": parent_line.sequence,
                        "parent_line_id": parent_id,
                    }
                )
            total_price += line.quantity * line.price
        parent_line.write({"price_unit": total_price})
