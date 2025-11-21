from odoo import _, api, fields, models, Command

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model_create_multi
    def create(self, vals_list):
        new_vals_list = []

        for vals in vals_list:
            new_vals_list.append(vals)

            order_id = vals.get("order_id")
            product_id = vals.get("product_id")
            if order_id and product_id:
                order = self.env["sale.order"].browse(order_id)
                product = self.env["product.product"].browse(product_id)

                if product.product_tmpl_id.has_deposit:
                    deposit_product = order.company_id.deposit_id.filtered(lambda d: d.id == product_id)
                    if deposit_product:
                        new_vals_list.append({
                            "order_id": order_id,
                            "product_id": deposit_product.id,
                            "product_uom_qty": vals.get("product_uom_qty", 1),
                            "price_unit": product.product_tmpl_id.amount,
                            "name": f"Deposit for {product.product_tmpl_id.name}",
                        })

        return super(SaleOrderLine, self).create(new_vals_list)
    