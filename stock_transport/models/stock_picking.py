from odoo import fields, models


class Picking(models.Model):
    _inherit = 'stock.picking'

    volume = fields.Float(compute="_compute_volume")

    def _compute_volume(self):
        for record in self:
            for move_line in record.move_ids:
                record.volume = record.volume + move_line.quantity * move_line.product_id.volume
