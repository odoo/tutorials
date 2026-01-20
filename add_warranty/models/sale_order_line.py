from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_warranty_sale_line_id = fields.Many2one('sale.order.line', default = None, help = "Store warranty sale line id in main product")

    # Unlink warranty if main product is deleted
    @api.ondelete(at_uninstall=False)
    def _unlink_warranty_line(self):
        for record in self:
            if record.product_warranty_sale_line_id:
                record.product_warranty_sale_line_id.unlink()
