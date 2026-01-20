from odoo import api, models, fields


class SaleOrderLineRentalInherit(models.Model):
    _inherit = "sale.order.line"
    main_rental_id = fields.Many2one("sale.order.line", ondelete="cascade")
    child_rental_id = fields.Many2one("sale.order.line", ondelete="cascade")

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        deposit_product_id = (
            self.env["ir.config_parameter"].sudo().get_param("rental.deposite_product")
        )
        for line in res:
            if (
                deposit_product_id
                and line.product_template_id.require_deposite
                and line.product_template_id.deposite_amount
            ):
                child_rental_ol = self.env["sale.order.line"].create(
                    {
                        "order_id": line.order_id.id,
                        "product_id": (int)(deposit_product_id),
                        "name": f"Deposit for {line.product_id.name}",
                        "product_uom_qty": line.product_uom_qty,
                        "price_unit": line.product_template_id.deposite_amount,
                        "main_rental_id": line.id,
                    }
                )
                line.child_rental_id = child_rental_ol.id
        return res

    def write(self, vals):
        for line in self:
            if line.child_rental_id and "product_uom_qty" in vals:
                qty = vals["product_uom_qty"]
                line.child_rental_id.write(
                    {
                        "product_uom_qty": qty,
                        "price_unit": line.product_template_id.deposite_amount,
                    }
                )
        return super().write(vals)
