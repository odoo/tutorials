from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model_create_multi
    def create(self, vals_list):
        """Create deposit lines automatically for products that require a deposit."""
        lines = super().create(vals_list)

        deposit_product_id = self.env['ir.config_parameter'].sudo().get_param('rental_deposit.deposit_product_id')
        if not deposit_product_id:
            raise UserError(_("Please select deposit product from configuration"))

        deposit_product = self.env["product.product"].browse(int(deposit_product_id))

        deposit_lines = []
        for line in lines:
            if line.product_id and line.product_id.product_tmpl_id.require_deposit:
                deposit_price = line.product_id.product_tmpl_id.deposit_amount if line.product_id.product_tmpl_id.deposit_amount else deposit_product.lst_price
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
        """Update deposit lines when the main product quantity changes."""
        lines = super().write(vals_list)

        deposit_product_id = self.env['ir.config_parameter'].sudo().get_param('rental_deposit.deposit_product_id')
        if not deposit_product_id:
            raise UserError(_("Please select a deposit product from configuration."))

        deposit_product = self.env['product.product'].browse(int(deposit_product_id))

        deposit_lines = []
        for line in self:
            existing_deposit_line = self.env['sale.order.line'].search([
                ("order_id", "=", line.order_id.id),
                ("linked_line_id", "=", line.id),
                ("product_id", "=", deposit_product.id)
            ], limit=1)

            if line.product_id and line.product_id.product_tmpl_id.require_deposit:
                deposit_price = line.product_id.product_tmpl_id.deposit_amount or deposit_product.lst_price
                if existing_deposit_line:
                    existing_deposit_line.write({
                        "product_uom_qty": line.product_uom_qty,
                        "price_unit": deposit_price,
                    })
                else:
                    deposit_lines.append({
                        "order_id": line.order_id.id,
                        "product_id": deposit_product.id,
                        "name": f"Deposit for {line.product_id.name}",
                        "product_uom_qty": line.product_uom_qty,
                        "price_unit": deposit_price,
                        "linked_line_id": line.id,
                    })
            elif existing_deposit_line:
                existing_deposit_line.unlink()

        if deposit_lines:
            self.create(deposit_lines)

        return lines
