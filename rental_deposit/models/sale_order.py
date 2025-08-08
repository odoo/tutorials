from odoo import _, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def _cart_update_order_line(self, product_id, quantity, order_line, **kwargs):
        res = super()._cart_update_order_line(product_id, quantity, order_line, **kwargs)
        return res[0] if len(res) else res
