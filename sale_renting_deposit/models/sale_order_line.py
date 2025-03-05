from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model_create_multi
    def create(self, values_list):
        res = super().create(values_list)
        deposit_lines = []
        for res_line in res:
            if res_line.order_id and res_line.product_id.rent_ok and res_line.product_id.require_deposit:
                deposit_product_id = self.env["ir.config_parameter"].sudo().get_param("rental.deposit_product_id")
                if deposit_product_id:
                    deposit_product = self.env["product.product"].browse(int(deposit_product_id))
                    existing_deposit_line = self.env["sale.order.line"].search([
                        ("order_id", "=", res_line.order_id.id),
                        ("product_id", "=", deposit_product.id),
                        ("name", "like", res_line.product_id.name)
                    ], limit=1)
                    if not existing_deposit_line:
                        deposit_lines.append({
                            "order_id": res_line.order_id.id,
                            "product_id": deposit_product.id,
                            "name": deposit_product.name + " for " + res_line.product_id.name,
                            "product_uom_qty": res_line.product_uom_qty,
                            "price_unit": res_line.product_id.deposit_product_amount,
                        })
        if deposit_lines:
            self.env["sale.order.line"].create(deposit_lines)
        return res

    def write(self, values):
        res = super().write(values)

        deposit_lines = []
        for res_line in self:  # Iterate over self, not res
            if res_line.order_id and res_line.product_id.rent_ok and res_line.product_id.require_deposit:
                deposit_product_id = self.env["ir.config_parameter"].sudo().get_param("rental.deposit_product_id")
                if deposit_product_id:
                    deposit_product = self.env["product.product"].browse(int(deposit_product_id))
                    existing_deposit_line = self.env["sale.order.line"].search([
                        ("order_id", "=", res_line.order_id.id),
                        ("product_id", "=", deposit_product.id),
                        ("name", "like", res_line.product_id.name)
                    ], limit=1)
                    if not existing_deposit_line:
                        deposit_lines.append({
                            "order_id": res_line.order_id.id,
                            "product_id": deposit_product.id,
                            "name": deposit_product.name + " for " + res_line.product_id.name,
                            "product_uom_qty": res_line.product_uom_qty,
                            "price_unit": res_line.product_id.deposit_product_amount,
                        })
                    else:
                        existing_deposit_line.write({
                            "product_uom_qty": res_line.product_uom_qty,
                            "price_unit": res_line.product_id.deposit_product_amount,
                        })
        if deposit_lines:
            self.env["sale.order.line"].create(deposit_lines)

        return res

    def unlink(self):
        deposit_product_id = self.env["ir.config_parameter"].sudo().get_param("rental.deposit_product_id")

        if deposit_product_id:
            deposit_product = self.env["product.product"].browse(int(deposit_product_id))

            for res_line in self:
                if res_line.order_id and res_line.product_id.rent_ok and res_line.product_id.require_deposit:
                    deposit_line_to_remove = self.env["sale.order.line"].search([
                        ("order_id", "=", res_line.order_id.id),
                        ("product_id", "=", deposit_product.id),
                        ("name", "like", res_line.product_id.name)
                    ])
                    if deposit_line_to_remove:
                        deposit_line_to_remove.unlink()

        return super().unlink()
