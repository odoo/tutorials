from odoo import api, fields, models
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_deposit_line = fields.Boolean(default=False)
    parent_id = fields.Many2one(comodel_name="sale.order.line", ondelete='cascade', copy=False)
    child_ids = fields.One2many(comodel_name="sale.order.line", inverse_name="parent_id", copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        # fetch deposit product name from ip.config.setting
        deposit_product_id = self.env["ir.config_parameter"].sudo().get_param("deposit_in_rental_app.deposit_product_id")

        if not deposit_product_id:
            raise UserError("Set deposit product from setting")

        for line in res:
            # If product line product is deposit enable create new deposit line
            if line.product_id.require_deposit and line.product_id.deposit_amount:
                deposit_order_line = self.env['sale.order.line'].create({
                    "order_id": line.order_id.id,
                    "product_id": int(deposit_product_id),
                    "name": f"Deposit for {line.product_id.name}",
                    "product_uom_qty": line.product_uom_qty,
                    "price_unit": line.product_template_id.deposit_amount,
                    "parent_id": line.id,
                    "sequence": line.sequence + 1,
                    "is_deposit_line": True,
                })

                if not deposit_order_line:
                    raise UserError("Something went wrong!!")

        return res

    def write(self, vals):
        res = super().write(vals)
        # Update quantity if deposit order line is already created
        if 'product_uom_qty' in vals:
            for line in self:
                if line.child_ids:
                    line.child_ids.write({
                        "product_uom_qty": vals['product_uom_qty'],
                        "price_unit": line.child_ids.price_unit
                    })
        return res
