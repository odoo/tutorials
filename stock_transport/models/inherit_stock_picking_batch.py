from odoo import api, fields, models


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    dock_id = fields.Many2one("stock.transport.dock", "Dock")
    vehicle_id = fields.Many2one("fleet.vehicle", "Vehicle")
    vehicle_category_id = fields.Many2one("fleet.vehicle.model.category", compute="_compute_vehicle_category", string="Vehicle Category", store=True)
    weight = fields.Float(string="Weight", compute="_compute_weight", store=True)
    volume = fields.Float(string="Volume", compute="_compute_volume", store=True)
    transfer_counts = fields.Integer("Transfer Counts", compute="_compute_transfer_counts", store=True)

    @api.depends("picking_ids.weight", "vehicle_category_id")
    def _compute_weight(self):
        for record in self:
            total_weight = 0.0
            for picking in record.picking_ids:
                total_weight = total_weight + picking.weight
            max_weight = record.vehicle_category_id.max_weight or 1.0
            record.weight = (total_weight / max_weight) * 100

    @api.depends("picking_ids.volume", "vehicle_category_id")
    def _compute_volume(self):
        for record in self:
            total_volume = 0.0
            for picking in record.picking_ids:
                total_volume = total_volume + picking.volume
            max_volume = record.vehicle_category_id.max_volume or 1.0
            record.volume = (total_volume / max_volume) * 100

    @api.depends("vehicle_id")
    def _compute_vehicle_category(self):
        for record in self:
            record.vehicle_category_id = record.vehicle_id.category_id if record.vehicle_id else False

    @api.depends("picking_ids")
    def _compute_transfer_counts(self):
        for record in self:
            record.transfer_counts = len(record.picking_ids)

    def _compute_display_name(self):
        res = super()._compute_display_name()
        for record in self:
            record.display_name = f"{record.name}: {record.weight}kg, {record.volume}m³"
        return res
