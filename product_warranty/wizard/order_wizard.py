from odoo import api, fields, models
from odoo.exceptions import UserError


class OrderWizard(models.TransientModel):
    _name = "order.wizard"
    _description = "Order Wizard"

    order_line_ids = fields.One2many(
        "product.warranty.wizard", "wizard_id", string="Order Lines"
    )

    @api.model
    def default_get(self, fields_list):
        res = super(OrderWizard, self).default_get(fields_list)
        order_lines = self.env["sale.order"].browse(self.env.context.get("active_id"))
        filter_oder_lines = order_lines.order_line.filtered(
            lambda l: l.product_template_id.is_warranty_available
        )
        order_lines = []
        if len(filter_oder_lines) == 0:
            raise UserError("No order line to divide cost")
        for line in filter_oder_lines:
            order_lines.append(
                (
                    0,
                    0,
                    {
                        "order_line_id": line.id,
                        "product_template_id": line.product_template_id.id,
                    },
                )
            )
        res["order_line_ids"] = order_lines
        return res

    def action_add_warranty(self):
        for line in self.order_line_ids:
            if line.year:
                self.env["sale.order.line"].create(
                    {
                        "product_template_id": line.year.product_template_id,
                        "price_unit": (
                            line.order_line_id.price_unit * line.year.percentage
                        )
                        / 100,
                        "name": f"Warranty for {line.order_line_id.name} (Ends: {line.end_date})",
                        "order_id": line.order_line_id.order_id.id,
                        "connected_order_line_id": line.order_line_id.id,
                    }
                )
