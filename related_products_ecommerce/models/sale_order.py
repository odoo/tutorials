from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _cart_update(self, product_id, line_id=None, add_qty=1, set_qty=0, **kwargs):
        res = super()._cart_update(product_id, line_id, add_qty, set_qty, **kwargs)
        product = self.env["product.product"].browse(product_id)

        actual_product_line = self.order_line.filtered(lambda l: l.product_id.id == product_id)
        actual_qty = sum(actual_product_line.mapped("product_uom_qty"))

        related_lines = self.order_line.filtered(
            lambda l: l.is_related_product and 
                l.product_id.product_tmpl_id in product.product_tmpl_id.related_product_ids
        )

        if actual_qty == 0:
            related_lines.unlink()
            return res

        if related_lines:
            related_lines.product_uom_qty = actual_qty

        pending_products = product.product_tmpl_id.related_product_ids - related_lines.product_id.product_tmpl_id
        for related_product in pending_products:
            order_line = self.env["sale.order.line"].create({
                "order_id": self.id,
                "product_id": related_product.product_variant_id.id,
                "product_uom_qty": actual_qty,
                "is_related_product": True,
            })

        return res
