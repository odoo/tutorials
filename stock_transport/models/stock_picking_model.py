from odoo import api, fields, models

class StockPicking(models.Model):
    _inherit = "stock.picking"

    volume = fields.Float(compute="_compute_volume", string="Volume", store=True)

    @api.depends('move_ids.product_id.volume', 'move_ids', 'move_ids.quantity')
    def _compute_volume(self):
        for record in self:
            total_volume = 0
            for move_id in record.move_ids:
                total_volume = total_volume + (move_id.quantity * move_id.product_id.volume)
            record.volume= total_volume
