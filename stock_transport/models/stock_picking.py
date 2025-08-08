from odoo import fields, models, api


class Picking(models.Model):
    _inherit = 'stock.picking'

    volume = fields.Float(compute="_compute_volume")

    @api.depends('move_ids.product_id.volume')
    def _compute_volume(self):
        for record in self:
            total_volume = 0
            for move_line in record.move_ids:
                total_volume = total_volume + move_line.quantity * move_line.product_id.volume
            record.volume = total_volume
