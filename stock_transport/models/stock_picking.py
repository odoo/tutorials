from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    volume = fields.Float(compute='_compute_volume')

    @api.depends('move_ids', 'move_ids.product_id', 'move_ids.quantity', 'move_ids.product_id.volume')
    def _compute_volume(self):
        for record in self:
            volume = 0
            for move in record.move_ids:
                qty = move.quantity
                volume = volume + (move.product_id.volume)*qty
            record.volume = volume
