from odoo import Command, api, fields, models


class AddWarrantyWizard(models.TransientModel):
    _name = "product.add.warranty"
    _description = "product.warranty.configuration"

    order_id = fields.Many2one(
        "sale.order", string="Sales Order", required=True, ondelete="cascade"
    )
    warranty_line_ids = fields.One2many(
        "add.warranty.line", "wizard_id", string="Warranty Lines"
    )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        order_id = self.env.context.get("active_id")

        if not order_id:
            return res

        order = self.env["sale.order"].browse(order_id)

        if not order.exists():
            return res

        warranty_lines = []
        for line in order.order_line:
            if line.product_id.is_warranty and not line.linked_line_ids:
                warranty_lines.append(
                    {"order_line_id": line.id, "product_id": line.product_id.id}
                )

        res.update(
            {
                "order_id": order.id,
                "warranty_line_ids": [Command.clear()]
                + [Command.create(vals) for vals in warranty_lines],
            }
        )

        return res


    def action_confirm(self):
        """Add selected warranties as sale order lines"""
        order_lines = []
        for line in self.warranty_line_ids:
            if not line.warranty_id:
                continue
            warranty_price = (
                line.order_line_id.price_unit * line.warranty_id.percentage / 100
            )
            order_lines.append(
                {
                    "product_id": line.warranty_id.product_id.product_variant_id.id,
                    "order_id": self.order_id.id,
                    "name": f" Extended Warranty, \n End Date: {line.end_date}",
                    "price_unit": warranty_price,
                    "product_uom_qty": 1,
                    "linked_line_id": line.order_line_id.id,
                }
            )

        if len(order_lines) > 0:
            self.env["sale.order.line"].create(order_lines)
        return
