from odoo import models, fields, api
from odoo.exceptions import UserError


class AddWarranty(models.TransientModel):
    _name = "add.warranty"

    warranty_line_ids = fields.One2many("add.warranty.line", "warranty_id", string="Products")

    @api.model
    def default_get(self, fields):
        defaults = super().default_get(fields)
        active_id = self.env.context.get("active_id")
        sale_order_lines = self.env["sale.order.line"].search(
            [("order_id", "=", active_id)]
        )
        product_lines = []
        for line in sale_order_lines:
            if line.product_template_id.is_warranty_available:
                product_lines.append(
                    (0, 0, {"product_id": line.product_id.id})
                )

        defaults["warranty_line_ids"] = product_lines

        return defaults

    def action_add_waranty_product(self):
        active_id = self.env.context.get("active_id")
        sale_order = self.env["sale.order"].browse(active_id)

        for record in self.warranty_line_ids:
            if record.year:
                oreder_line = sale_order.order_line.filtered(lambda line: line.product_id == record.product_id)
                price = (oreder_line.price_subtotal * record.year.percentage) / 100
                sale_order.order_line.create({
                            "product_id": record.year.product_id.id,
                            "name": f"{record.year.product_id.name}\n End Date: {record.end_date.strftime('%d/%m/%Y')}",
                            "order_id": sale_order.id,
                            "product_uom": 1,
                            "product_uom_qty": 1,
                            "price_unit": price,
                            "tax_id": None,
                            "waranty_with_products": record.id,
                        },)
                