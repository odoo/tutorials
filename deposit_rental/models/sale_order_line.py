from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_deposit_line = fields.Boolean(default=False)
    deposit_link_id = fields.Many2one("sale.order.line", ondelete="cascade")

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)

        for line in lines:
            deposit_product = line.order_id.company_id.deposit_product_id 

            if deposit_product and line.product_template_id.deposit_amount > 0 and not line.is_deposit_line:
                deposit_line_vals = {
                    "order_id": line.order_id.id,
                    "product_id": deposit_product.id,
                    "product_uom_qty": line.product_uom_qty,
                    "price_unit": line.product_template_id.deposit_amount,  
                    "is_deposit_line": True,
                    "sequence": line.sequence + 1,
                    "deposit_link_id": line.id,
                    "name": f"Deposit for {line.name}",
                }
                self.create(deposit_line_vals)

        return lines

    def write(self, vals):
        res = super().write(vals)
        if "product_uom_qty" in vals:
            for line in self:
                if not line.is_deposit_line:
                    deposit_line = self.search([
                        ("order_id", "=", line.order_id.id),
                        ("deposit_link_id", "=", line.id),
                    ])
                    if deposit_line:
                        deposit_line.write({
                            "product_uom_qty": vals["product_uom_qty"],
                            "price_unit": line.product_template_id.deposit_amount,
                        })
        return res
