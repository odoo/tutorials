from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_deposit_line = fields.Boolean(default=False)
    deposit_link_id = fields.Many2one("sale.order.line", ondelete="cascade")

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)

        deposit_product = self.env.company.product_deposit
        deposit_lines = []
        for line in lines:
            if (line.product_id == deposit_product) and line.product_id.product_tmpl_id.required_deposit:
                deposit_price = line.product_id.product_tmpl_id.amount_deposit * line.product_uom_qty
                deposit_lines.append({
                    "is_deposit_line": True,
                    "order_id": line.order_id.id,
                    "product_id": deposit_product.id,
                    "name": f"Deposit for {line.product_id.name}",
                    "product_uom_qty": line.product_uom_qty,
                    "price_unit": deposit_price,
                    "deposit_link_id": line.id,
                })
        if deposit_lines:
            super().create(deposit_lines)
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
                            "price_unit": line.product_template_id.amount_deposit,
                        })
        return res
