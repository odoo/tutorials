from odoo import api, fields, models


class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'

    dock_id = fields.Many2one(
        'dock',
    )

    vehicle_id = fields.Many2one(
        'fleet.vehicle',
    )

    vehicle_category_id = fields.Many2one(
        'fleet.vehicle.model.category',
        compute='_compute_vehicle_category',
        string="Vehicle Category",
    )

    weight_progress = fields.Float(compute='_compute_total_weight', default=0)
    volume_progress = fields.Float(compute='_compute_total_volume', default=0)

    @api.depends('vehicle_id')
    def _compute_vehicle_category(self):
        for record in self:
            record.vehicle_category_id = record.vehicle_id.category_id.id

    @api.depends('picking_ids.weight', 'picking_ids')
    def _compute_total_weight(self):
        for record in self:
            total_weight = 0
            for picking_id in record.picking_ids:
                total_weight = total_weight + picking_id.weight
            if record.vehicle_category_id.max_weight != 0:
                record.weight_progress = 100 * total_weight / record.vehicle_category_id.max_weight
            else:
                record.weight_progress = 0.0

    @api.depends('picking_ids.volume', 'picking_ids')
    def _compute_total_volume(self):
        for record in self:
            total_volume = 0
            for picking_id in record.picking_ids:
                total_volume = total_volume + picking_id.volume
            if record.vehicle_category_id.max_volume != 0:
                record.volume_progress = 100 * total_volume / record.vehicle_category_id.max_volume
            else:
                record.volume_progress = 0.0
