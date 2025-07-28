from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_warranty_sale_line_id = fields.Many2one(
        'sale.order.line',
        ondelete="cascade",
        )

    @api.ondelete(at_uninstall=False)
    def _unlink_warranty_line(self):
        for record in self:
            if record.product_warranty_sale_line_id:
                record.product_warranty_sale_line_id.unlink()
