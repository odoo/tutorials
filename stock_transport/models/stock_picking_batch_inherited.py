from odoo import api, fields, models

from datetime import date


class stockPickingBatchInherited(models.Model):
    _inherit = 'stock.picking.batch'
    _rec_name = 'name'

    dock_id = fields.Many2one('dock')
    vehicle_id = fields.Many2one('fleet.vehicle')
    vehicle_category_id = fields.Many2one('fleet.vehicle.model.category', compute='_compute_category', store=True)
    weight = fields.Float(compute="_compute_weight")
    volume = fields.Float(compute="_compute_volume")
    total_weight = fields.Float(compute="_compute_total_weight_volume", store=True)
    total_volume = fields.Float(compute="_compute_total_weight_volume", store=True)
    transfer = fields.Integer(compute='_compute_transfer', store=True)
    lines = fields.Integer(compute='_compute_lines', store=True)

    def _compute_display_name(self):
        for record in self:
            record.display_name = "{}: {}Kg, {}m3".format(record.name, record.weight, record.volume)

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
                    weight = weight + (move.product_id.weight)*qty
                    volume = volume + (move.product_id.volume)*qty
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
            if not max_weight == 0:
                record.weight = (weight/max_weight)*100
            else:
                record.weight = 0

    @api.depends('picking_ids', 'picking_ids.move_ids', 'picking_ids.move_ids.product_id', 'picking_ids.move_ids.product_id.volume')
    def _compute_volume(self):
        for record in self:
            volume = 0
            max_volume = record.vehicle_id.category_id.max_volume
            for pick in record.picking_ids:
                for move in pick.move_ids:
                    qty = move.quantity
                    volume = volume + (move.product_id.volume)*qty
            if not max_volume == 0:
                record.volume = (volume/max_volume)*100
            else:
                record.volume = 0

    @api.depends('picking_ids')
    def _compute_transfer(self):
        for record in self:
            transfers = 0
            for pick in record.picking_ids:
                transfers = transfers + 1
            record.transfer = transfers

    @api.depends('picking_ids', 'picking_ids.move_ids')
    def _compute_lines(self):
        for record in self:
            lines = 0
            for pick in record.picking_ids:
                for move in pick.move_ids:
                    lines = lines + 1
            record.lines = lines
