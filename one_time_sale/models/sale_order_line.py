from odoo import models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _get_pricelist_price(self):
        """Return the product's list price if the order line has one time purchase product without any plan."""
        self.ensure_one()
        self.product_id.ensure_one()

        if self.recurring_invoice and not self.order_id.plan_id:
            price = self.pricelist_item_id._compute_price(
                product=self.product_id.with_context(**self._get_product_price_context()),
                quantity=self.product_uom_qty or 1.0,
                uom=self.product_uom,
                date=self.order_id.date_order,
                currency=self.currency_id,
            )

            return price

        return super()._get_pricelist_price() or self.price_unit
