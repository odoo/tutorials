from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    weight = fields.Float(compute='_compute_weight', default=0, string="Weight for shipping", store=True, groups="stock_transport.group_stock_transport_admin")
    volume = fields.Float(compute='_compute_volume', default=0, string="Volume", store=True, groups="stock_transport.group_stock_transport_admin")

    @api.depends('move_ids', 'move_ids.quantity', 'move_ids.product_id.weight')
    def _compute_weight(self):
        for record in self:
            total_weight = 0
            for move_id in record.move_ids:
                total_weight = total_weight + move_id.quantity * move_id.product_id.weight
            record.weight = total_weight

    @api.depends('move_ids', 'move_ids.quantity', 'move_ids.product_id.volume')
    def _compute_volume(self):
        for record in self:
            total_volume = 0
            for move_id in record.move_ids:
                total_volume = total_volume + move_id.quantity * move_id.product_id.volume
            record.volume = total_volume
