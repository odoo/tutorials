from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    volume = fields.Float(string="Volume", compute="_compute_volume")
    
    @api.depends('move_ids_without_package.product_uom_qty', 'move_ids_without_package.product_id.volume')
    def _compute_volume(self):
        for records in self:
            records.volume = sum(records.move_ids_without_package.mapped(lambda moves: moves.product_uom_qty * moves.product_id.volume))
