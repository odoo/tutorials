from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    delivered_percent = fields.Float(
        string="Delivered (%)",
        compute="_compute_delivered_percent",
        inverse="_inverse_delivered_percent",
        store=True,
        digits=(16, 2)
    )

    @api.depends(
        'product_uom_qty',
        'qty_delivered',
        'product_id.product_tmpl_id.service_manual_delivery'
    )
    def _compute_delivered_percent(self):
        for line in self:
            if (
                line.product_id.product_tmpl_id.service_manual_delivery
                and line.product_uom_qty
            ):
                line.delivered_percent = (line.qty_delivered / line.product_uom_qty) * 100
            else:
                line.delivered_percent = 0.0

    def _inverse_delivered_percent(self):
        for line in self:
            if (
                line.product_id.product_tmpl_id.service_manual_delivery
                and line.product_uom_qty
            ):
                line.qty_delivered = (line.delivered_percent / 100) * line.product_uom_qty
