from odoo import fields, models, api


class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'

    dock_id = fields.Many2one('stock.transport.dock', string="Dock")
    vehicle_id = fields.Many2one('fleet.vehicle',string="Vehicle")
    category_id = fields.Many2one('fleet.vehicle.model.category', string="Vehicle Category", compute="_compute_vehicle_category", store=True)
    weight = fields.Float(compute="_compute_weight", store=True)
    volume = fields.Float(compute="_compute_volume", store=True)
    transfer_count = fields.Integer(compute="_compute_transfers", store=True)

    @api.depends('category_id')
    def _compute_display_name(self):
        for record in self:
            name = f"{record.name} {record.category_id.display_name}"
            record.display_name = name

    @api.depends('picking_ids')
    def _compute_transfers(self):
        for records in self:
            records.transfer_count = len(records.picking_ids)

    @api.depends('picking_ids.shipping_weight', 'category_id.max_weight')
    def _compute_weight(self):
        for records in self:
            if records.category_id.max_weight != 0:
                records.weight = 100 * (sum(records.picking_ids.mapped('shipping_weight')) / records.category_id.max_weight)
            else:
                records.weight = 0

    @api.depends('picking_ids.volume', 'category_id.max_volume')
    def _compute_volume(self):
        for records in self:
            if records.category_id.max_volume != 0:
                records.volume = 100 * (sum(records.picking_ids.mapped('volume')) / records.category_id.max_volume)
            else:
                records.volume = 0

    @api.depends('vehicle_id.category_id')
    def _compute_vehicle_category(self):
        for records in self:
            if records.vehicle_id:
                records.category_id = records.vehicle_id.category_id
