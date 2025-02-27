from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model_create_multi
    def create(self, vals_list):
        lines = super(SaleOrderLine, self).create(vals_list)
        deposit_product_id = self.env['ir.config_parameter'].sudo().get_param('rental_deposit.deposit_product_id')
        deposit_product = self.env["product.product"].browse(int(deposit_product_id))
        deposit_lines = []
        for line in lines:
            if line.product_id and line.product_id.product_tmpl_id.require_deposit:
                if not deposit_product_id:
                    raise UserError(_("Please select deposit product from configuration"))
                deposit_price = line.product_id.product_tmpl_id.deposit_amount if line.product_id.product_tmpl_id.deposit_amount else deposit_product.lst_price
                existing_deposit_lines = self.env["sale.order.line"].search([
                    ("order_id", "=", line.order_id.id),
                    ("product_id", "=", deposit_product.id),
                    ("linked_line_id", "=", line.id)
                ], limit=1)
                if not existing_deposit_lines:
                    deposit_lines.append({
                        "order_id": line.order_id.id,
                        "product_id": deposit_product.id,
                        "name": f"Deposit for {line.product_id.name}",
                        "product_uom_qty": line.product_uom_qty,
                        "price_unit": deposit_price,
                        "linked_line_id": line.id,
                    })
        if deposit_lines:
            self.create(deposit_lines)
        return lines

    def write(self, vals_list):
        lines = super(SaleOrderLine, self).write(vals_list)

        deposit_product_id = self.env["ir.config_parameter"].sudo().get_param("rental_deposit.deposit_product_id")
        deposit_product = self.env["product.product"].browse(int(deposit_product_id))

        for line in self:
            deposit_line = self.env["sale.order.line"].search([
                ("order_id", "=", line.order_id.id),
                ("linked_line_id", "=", line.id),
                ("product_id", "=", deposit_product.id)
            ], limit=1)

            if line.product_id and line.product_id.product_tmpl_id.require_deposit:
                if not deposit_product_id:
                    raise UserError(_("Please select a deposit product from configuration."))
                deposit_price = line.product_id.product_tmpl_id.deposit_amount or deposit_product.lst_price
                if deposit_line:
                    deposit_line.write({
                        "product_uom_qty": line.product_uom_qty,
                        "price_unit": deposit_price,
                    })
                else:
                    self.create({
                        "order_id": line.order_id.id,
                        "product_id": deposit_product.id,
                        "name": f"Deposit for {line.product_id.name}",
                        "product_uom_qty": line.product_uom_qty,
                        "price_unit": deposit_price,
                        "linked_line_id": line.id,
                    })

            elif deposit_line:
                deposit_line.unlink()

        return lines
