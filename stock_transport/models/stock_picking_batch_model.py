from odoo import api, fields, models

class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"
    
    dock_id = fields.Many2one(
        "dock", 
        "Dock"
    )

    vehicle_id = fields.Many2one(
        "fleet.vehicle",
        "Vehicle",
    )

    vehicle_category_id = fields.Many2one(
        "fleet.vehicle.model.category",
        compute="_compute_vehicle_category"
    )

    weight_bar = fields.Float(
        compute='_compute_weight', 
        default=0
    )

    volume_bar = fields.Float(
        compute='_compute_volume', 
        default=0
    )

    @api.depends("vehicle_id")
    def _compute_vehicle_category(self):
        for record in self:
            record.vehicle_category_id = record.vehicle_id.category_id.id

    @api.depends('picking_ids', 'picking_ids.volume')
    def _compute_volume(self):
        for record in self:
            total_volume = 0
            for picking_id in record.picking_ids:
                total_volume = total_volume + picking_id.volume
            if record.vehicle_category_id.max_volume != 0:
                record.volume_bar = (total_volume/ record.vehicle_category_id.max_volume) * 100
                # print(total_volume, "Vollll  ", record.vehicle_category_id.max_volume)
            else:
                record.volume_bar = 0.0
    
    @api.depends('picking_ids', 'picking_ids.move_ids', 'picking_ids.move_ids.product_id.weight')
    def _compute_weight(self):
        for record in self:
            max_weight = record.vehicle_category_id.max_weight
            total_weight = 0
            for picking_id in record.picking_ids:
                for move_id in picking_id.move_ids:
                    total_weight = total_weight + move_id.product_id.weight * move_id.quantity
            if max_weight == 0:
                record.weight_bar = 0.0
            else:
                record.weight_bar = (total_weight / max_weight) * 100
