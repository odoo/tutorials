from odoo import api, fields, models
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_line_with_deposit = fields.Many2one("sale.order.line", ondelete="cascade")

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for line in res:
            self._create_deposit_line(line)
        return res

    def write(self, vals):
        res = super().write(vals)
        for line in self:
            deposit_line = self.search([("product_line_with_deposit", "=", line.id)])
            if deposit_line:
                if "product_uom_qty" in vals:
                    deposit_amount = (
                        line.product_id.deposit_amount * line.product_uom_qty
                    )
                    deposit_line.write({"price_unit": deposit_amount})
                if "product_id" in vals and line.product_id.require_deposit:
                    self._create_deposit_line(line)
                    deposit_line.unlink()
                if "product_id" in vals and not line.product_id.require_deposit:
                    deposit_line.unlink()
        return res

    def _create_deposit_line(self, line):
        if line.product_id.require_deposit:
            deposit_product = line.order_id.company_id.deposit_product_id
            if not deposit_product:
                raise UserError("No deposit product configured.")
            deposit_amount = line.product_id.deposit_amount * line.product_uom_qty
            self.env["sale.order.line"].create(
                {
                    "order_id": line.order_id.id,
                    "sequence": line.sequence + 1,
                    "product_id": deposit_product.id,
                    "name": f"Added for {line.product_id.name}",
                    "price_unit": deposit_amount,
                    "product_uom_qty": 1,
                    "product_line_with_deposit": line.id,
                }
            )
