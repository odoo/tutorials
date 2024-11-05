from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    weight = fields.Float(string="Weight", store=True)
    volume = fields.Float(compute="_calculate_volume", string="Volume", store=True)

    @api.depends("product_id", "product_id.volume", "move_line_ids.quantity")
    def _calculate_volume(self):
        for record in self:
            total_volume = 0.0
            for move in record.move_line_ids:
                if move.product_id:
                    total_volume = total_volume + (move.product_id.volume * move.quantity)
            record.volume = total_volume
