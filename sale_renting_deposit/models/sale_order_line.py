from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_deposit_line = fields.Boolean(default=False)
    linked_line_id = fields.Many2one(
        "sale.order.line", string="Linked Line", ondelete="cascade"
    )

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        rental_lines = lines.filtered(
            lambda l: l.product_id.is_deposit_required and not l.is_deposit_line
        )
        deposit_vals = []
        for line in rental_lines:
            deposit_vals.append(
                {
                    "order_id": line.order_id.id,
                    "product_id": line.company_id.deposit_product.id,
                    "product_uom_qty": 1,
                    "price_unit": line.product_id.deposit_amount * line.product_uom_qty,
                    "name": f"This amount is deposit for {line.product_id.name} product",
                    "is_deposit_line": True,
                    "linked_line_id": line.id,
                }
            )
        if deposit_vals:
            self.env["sale.order.line"].create(deposit_vals)
        return lines

    def write(self, vals):
        res = super().write(vals)
        if "product_uom_qty" in vals or "product_id" in vals:
            for line in self:
                deposit = self.env["sale.order.line"].search(
                    [("linked_line_id", "=", line.id)]
                )
                if deposit:
                    if line.product_id.is_deposit_required:
                        deposit.write(
                            {
                                "price_unit": line.product_id.deposit_amount
                                * line.product_uom_qty
                            }
                        )
                    else:
                        deposit.unlink()
        return res

    @api.ondelete(at_uninstall=False)
    def _unlink_order_line(self):
        deposits = self.env["sale.order.line"].search(
            [("linked_line_id", "in", self.ids)]
        )
        if deposits:
            deposits.unlink()
