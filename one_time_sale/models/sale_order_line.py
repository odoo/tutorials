from odoo import models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _get_pricelist_price(self):
        """Return the product's list price if the order line has one time purchase product without any plan."""
        if self.recurring_invoice and not self.order_id.plan_id:
            return self.product_template_id.list_price
        
        return super()._get_pricelist_price() or self.price_unit
