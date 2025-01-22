from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_deposit_line = fields.Boolean(string="Is Deposit Line", default=False)
    deposit_link_id = fields.Many2one(
        "sale.order.line",
        string="Original Sale Order Line",
        ondelete="cascade"
    )

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)

        for line in lines:
            if line.product_template_id.deposit_amount > 0 and not line.is_deposit_line:
                deposit_product = self.env["product.template"].search([
                    ("name", "=", "Deposit")
                ], limit=1)

                if deposit_product:
                    self.create({
                        "order_id": line.order_id.id,
                        "product_template_id": deposit_product.id,
                        "product_uom_qty": line.product_uom_qty,
                        "price_unit": line.product_template_id.deposit_amount,
                        "is_deposit_line": True,
                        "deposit_link_id": line.id,
                        "name": f"Deposit for {line.name}",
                    })
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
