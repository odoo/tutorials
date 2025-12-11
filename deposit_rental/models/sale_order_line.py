from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_deposit_line = fields.Boolean(string="Is Deposit Line", default=False)

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)

        deposit_product_id = self.env["ir.config_parameter"].sudo().get_param("sale_renting.deposit_product_id")
        deposit_product = self.env["product.product"].sudo().browse(int(deposit_product_id)) if deposit_product_id else None

        for line in lines:
            if line.product_template_id.deposit_amount > 0 and not line.is_deposit_line and deposit_product:
                self.create({
                    "order_id": line.order_id.id,
                    "product_id": deposit_product.id,
                    "product_uom_qty": line.product_uom_qty,
                    "price_unit": line.product_template_id.deposit_amount,
                    "is_deposit_line": True,
                    "sequence": line.sequence + 1,
                    "linked_line_id": line.id,
                    "name": f"Deposit for {line.name}",
                })
        return lines

    def write(self, vals):
        res = super().write(vals)

        if "product_uom_qty" in vals:

            deposit_lines = self.search([
                ("order_id", "=", self.order_id.id),
                ("is_deposit_line", "=", True),
            ])

            for line in self - deposit_lines:
                deposit_line = deposit_lines.filtered(lambda deposit_line: deposit_line.linked_line_id.id == line.id)
                if deposit_line:
                    deposit_line.write({
                        "product_uom_qty": vals["product_uom_qty"],
                    })
        return res
