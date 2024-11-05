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
        store=True
    )

    weight_progress = fields.Float(compute='_compute_total_weight', default=0)
    volume_progress = fields.Float(compute='_compute_total_volume', default=0)

    weight = fields.Float(compute="_compute_weight_and_volume", store=True)
    volume = fields.Float(compute="_compute_weight_and_volume", store=True)
    transfers = fields.Integer(compute="_compute_transfers_and_lines", store=True)
    lines = fields.Integer(compute="_compute_transfers_and_lines", store=True)

    @api.depends('vehicle_id')
    def _compute_vehicle_category(self):
        for record in self:
            record.vehicle_category_id = record.vehicle_id.category_id.id

    @api.depends('picking_ids', 'picking_ids.weight')
    def _compute_total_weight(self):
        for record in self:
            total_weight = 0
            for picking_id in record.picking_ids:
                total_weight = total_weight + picking_id.weight
            if record.vehicle_category_id.max_weight != 0:
                record.weight_progress = 100 * total_weight / record.vehicle_category_id.max_weight
            else:
                record.weight_progress = 0.0

    @api.depends('picking_ids', 'picking_ids.volume')
    def _compute_total_volume(self):
        for record in self:
            total_volume = 0
            for picking_id in record.picking_ids:
                total_volume = total_volume + picking_id.volume
            if record.vehicle_category_id.max_volume != 0:
                record.volume_progress = 100 * total_volume / record.vehicle_category_id.max_volume
            else:
                record.volume_progress = 0.0

    @api.depends('picking_ids', 'picking_ids.move_ids')
    def _compute_transfers_and_lines(self):
        for record in self:
            total_lines = 0
            for picking_id in record.picking_ids:
                total_lines = total_lines + len(picking_id.move_ids)
            record.transfers = len(record.picking_ids)
            record.lines = total_lines

    @api.depends('picking_ids', 'picking_ids.weight', 'picking_ids.volume')
    def _compute_weight_and_volume(self):
        for record in self:
            total_weight = 0
            total_volume = 0
            for picking_id in record.picking_ids:
                total_weight = total_weight + picking_id.weight
                total_volume = total_volume + picking_id.volume
            record.weight = total_weight
            record.volume = total_volume

    def _compute_display_name(self):
        res = super()._compute_display_name()
        for record in self:
            record.display_name = f"{record.name}: {record.weight}(kg), {record.volume}(m³)"
        return res