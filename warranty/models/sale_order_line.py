from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.ondelete(at_uninstall=False)
    def _unlink_sale_order_line_warranty(self):
        for line in self:
            if line.linked_line_ids:
                line.linked_line_ids.unlink()
