from odoo import models,fields,api

class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'

    dock_id = fields.Many2one('stock.location',string='Dock')
    vehicle_id = fields.Many2one('fleet.vehicle',string='Vehicle')
    vehicle_category_id = fields.Many2one('fleet.vehicle.model.category',string='Vehicle Catagory')
    weight_percentage = fields.Float(string="Weight (%)", compute="_compute_weight_volume", store=True, invisible=not vehicle_category_id)
    volume_percentage = fields.Float(string="Volume (%)", compute="_compute_weight_volume", store=True, invisible=not vehicle_category_id)
    total_weight_display = fields.Float(compute="_compute_dynamic_totals")
    total_volume_display = fields.Float(compute="_compute_dynamic_totals")
    vehicle_weight_capacity = fields.Float(string="Vehcilce Payload Capacity",
                              related='vehicle_category_id.max_weight')
    vehicle_volume_capacity = fields.Float(string="Max Volume (m³)",
                              related='vehicle_category_id.max_volume')
    
    @api.depends('picking_ids.weight', 'picking_ids.volume')
    def _compute_dynamic_totals(self):
        for record in self:
            record.total_weight_display = sum(record.picking_ids.mapped('weight')) if record.picking_ids else 0
            record.total_volume_display = sum(record.picking_ids.mapped('volume')) if record.picking_ids else 0

    @api.depends('picking_ids', 'picking_ids.weight', 'picking_ids.volume', 'vehicle_category_id')
    def _compute_weight_volume(self):
        for record in self:
            total_weight = sum(record.picking_ids.mapped('weight'))
            total_volume = sum(record.picking_ids.mapped('volume'))
            max_weight = record.vehicle_category_id.max_weight or 1
            max_volume = record.vehicle_category_id.max_volume or 1

            record.weight_percentage = (total_weight / max_weight) * 100 if record.vehicle_category_id else 0
            record.volume_percentage = (total_volume / max_volume) * 100 if record.vehicle_category_id else 0
