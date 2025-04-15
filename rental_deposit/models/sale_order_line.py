from odoo import api, fields, models
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_ref_id = fields.Many2one("sale.order.line", ondelete='cascade', copy=False)
    product_deposit_ids = fields.One2many("sale.order.line", inverse_name="product_ref_id", copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)

        deposit_product_id = self.env["ir.config_parameter"].sudo().get_param("deposit_in_rental_app.deposit_product_id")
        if not deposit_product_id:
            raise UserError("Set deposit product from settings.")
        deposit_product_id = int(deposit_product_id)

        for line in res:
            if line.product_ref_id:
                continue

            if line.product_id.require_deposit and line.product_id.deposit_amount:
                deposit_amount = line.product_id.deposit_amount * line.product_uom_qty
                self.env['sale.order.line'].create({
                    "order_id": line.order_id.id,
                    "product_id": deposit_product_id,
                    "name": f"Deposit for {line.product_id.name}",
                    "product_uom_qty": 1,
                    "price_unit": deposit_amount,
                    "product_ref_id": line.id,
                    "sequence": line.sequence + 1,
                })
        return res

    def write(self, vals):
        res = super().write(vals)
        if 'product_uom_qty' in vals:
            for line in self:
                if line.product_ref_id:
                    continue
                deposit_line = line.product_deposit_ids
                if deposit_line:
                    new_deposit = line.product_id.deposit_amount * vals['product_uom_qty']
                    deposit_line.write({
                        "product_uom_qty": 1,
                        "price_unit": new_deposit,
                    })
        return res
