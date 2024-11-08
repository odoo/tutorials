from odoo import api, fields, models


class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'

    dock_id = fields.Many2one('dock.dock', groups="stock_transport.stock_transport_group_user_admin")
    vehicle_id = fields.Many2one('fleet.vehicle', groups="stock_transport.stock_transport_group_user_admin")
    vehicle_category_id = fields.Many2one('fleet.vehicle.model.category', compute='_compute_category', store=True, groups="stock_transport.stock_transport_group_user_admin")
    weight = fields.Float(compute="_compute_weight", groups="stock_transport.stock_transport_group_user_admin")
    volume = fields.Float(compute="_compute_volume", groups="stock_transport.stock_transport_group_user_admin")
    total_weight = fields.Float(compute="_compute_total_weight_volume", store=True, groups="stock_transport.stock_transport_group_user_admin")
    total_volume = fields.Float(compute="_compute_total_weight_volume", store=True, groups="stock_transport.stock_transport_group_user_admin")
    transfer = fields.Integer(compute='_compute_transfer', store=True, groups="stock_transport.stock_transport_group_user_admin")
    lines = fields.Integer(compute='_compute_lines', store=True, groups="stock_transport.stock_transport_group_user_admin")

    @api.depends('vehicle_id', 'vehicle_id.category_id')
    def _compute_category(self):
        for record in self:
            record.vehicle_category_id = record.vehicle_id.category_id

    @api.depends('picking_ids', 'picking_ids.move_ids', 'picking_ids.move_ids.product_id', 'picking_ids.move_ids.product_id.weight', 'picking_ids.move_ids.product_id.volume')
    def _compute_total_weight_volume(self):
        for record in self:
            weight = 0
            volume = 0
            for pick in record.picking_ids:
                for move in pick.move_ids:
                    qty = move.quantity
                    weight = weight + (move.product_id.weight) * qty
                    volume = volume + (move.product_id.volume) * qty
            record.total_weight = weight
            record.total_volume = volume

    @api.depends('picking_ids', 'picking_ids.move_ids', 'picking_ids.move_ids.product_id', 'picking_ids.move_ids.product_id.weight')
    def _compute_weight(self):
        for record in self:
            weight = 0
            max_weight = record.vehicle_id.category_id.max_weight
            for pick in record.picking_ids:
                for move in pick.move_ids:
                    qty = move.quantity
                    weight = weight + (move.product_id.weight)*qty
            record.weight = (weight/max_weight) * 100 if max_weight else 0

    @api.depends('picking_ids', 'picking_ids.move_ids', 'picking_ids.move_ids.product_id', 'picking_ids.move_ids.product_id.volume')
    def _compute_volume(self):
        for record in self:
            volume = 0
            max_volume = record.vehicle_id.category_id.max_volume
            for pick in record.picking_ids:
                for move in pick.move_ids:
                    qty = move.quantity
                    volume = volume + (move.product_id.volume) * qty
                record.volume = (volume/max_volume) * 100 if max_volume else 0

    @api.depends('picking_ids')
    def _compute_transfer(self):
        for record in self:
            record.transfer = len(record.picking_ids)

    @api.depends('picking_ids', 'picking_ids.move_ids')
    def _compute_lines(self):
        for record in self:
            record.lines = len(record.picking_ids.move_ids)
