from odoo import api, fields, models


class ProductKitWizard(models.TransientModel):
    _name = "product.kit.wizard"
    _description = "Kit Sub Product Wizard"

    sale_line_id = fields.Many2one("sale.order.line")
    main_product_id = fields.Many2one(
        "product.product",
        string="Product"
    )
    line_ids = fields.One2many(
        "product.kit.wizard.line",
        "wizard_id",
        string="Sub Products"
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        sale_line = self.env["sale.order.line"].browse(
            self.env.context.get("active_id")
        )

        if not sale_line.product_id:
            return res

        order = sale_line.order_id
        product = sale_line.product_id

        lines = []

        for sub_product in product.product_tmpl_id.sub_product:

            existing_line = order.order_line.filtered(
                lambda l:
                l.product_id == sub_product
                and l.kit_parent_line_id == sale_line
            )[:1]

            lines.append(
                (0, 0, {
                    "product_id": sub_product.id,
                    "quantity": (
                        existing_line.product_uom_qty
                        if existing_line else 1.0
                    ),
                    "price": (
                        existing_line.extra_price
                        if existing_line else sub_product.lst_price
                    ),
                })
            )

        res.update({
            "sale_line_id": sale_line.id,
            "main_product_id": product.id,
            "line_ids": lines,
        })

        return res

    def action_confirm(self):
        self.ensure_one()
        order = self.sale_line_id.order_id
        parent_line = self.sale_line_id
        total_price = parent_line.product_id.lst_price

        has_extra_price = 'extra_price' in self.env['sale.order.line']._fields

        for line in self.line_ids:
            existing_line = order.order_line.filtered(
                lambda l: l.product_id == line.product_id and l.kit_parent_line_id == parent_line
            )[:1]

            vals = {
                "name": line.product_id.display_name,
                "product_uom_qty": line.quantity,
                "price_unit": 0.0,
                "sequence": parent_line.sequence + 1,
            }

            if has_extra_price:
                vals["extra_price"] = line.price

            if existing_line:
                existing_line.write(vals)
            else:
                vals.update({
                    "order_id": order.id,
                    "product_id": line.product_id.id,
                    "is_kit_product": True,
                    "kit_parent_line_id": parent_line.id,
                })
                self.env["sale.order.line"].create(vals)

            total_price += line.quantity * line.price

        parent_line.write({"price_unit": total_price})

        return {"type": "ir.actions.act_window_close"}
