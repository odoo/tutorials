from odoo import models, fields, api
from odoo.exceptions import UserError


class AddWarranty(models.TransientModel):
    _name = "add.warranty"

    product_ids = fields.One2many("add.warranty.line", "warranty_id", string="Products")

    @api.model
    def default_get(self, fields):
        defaults = super().default_get(fields)
        active_id = self.env.context.get("active_id")
        if not active_id:
            raise UserError("No active_id found in context.")
        sale_order_lines = self.env["sale.order.line"].search(
            [("order_id", "=", active_id)]
        )

        if not sale_order_lines:
            raise UserError(
                f"No Sale Order Lines found for Sale Order with ID {active_id}."
            )

        product_lines = []
        for line in sale_order_lines:
            if line.product_template_id.is_warranty_available:
                product_lines.append(
                    (0, 0, {"product_template_id": line.product_template_id.id})
                )

        defaults["product_ids"] = product_lines

        return defaults

    def action_add_waranty_product(self):
        active_id = self.env.context.get("active_id")
        sale_order = self.env["sale.order"].browse(active_id)

        for line in self.product_ids:
            if line.year:
                price = 0
                for record in sale_order.order_line:
                    if record.product_template_id == line.product_template_id:
                        price = (record.price_subtotal * line.year.percentage) / 100
                        sale_order.order_line = [
                            (
                                0,
                                0,
                                {
                                    "product_id": line.year.product_id.id,
                                    "name": "Extended Warranty",
                                    "order_id": sale_order.id,
                                    "product_uom": 1,
                                    "product_uom_qty": 1,
                                    "price_unit": price,
                                    "tax_id": None,
                                    "waranty_with_products": record.id,
                                },
                            )
                        ]
