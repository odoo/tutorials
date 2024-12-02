from odoo import fields, models, api


class stockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'
    _rec_name = 'name'

    weight_percentage = fields.Float(compute="_compute_weight_percentage", string='Weight')
    volume_percentage = fields.Float(compute="_compute_volume_percentage", string='Volume')

    weight = fields.Float(string="Weight", compute="_compute_weight", store=True)
    volume = fields.Float(string="Volume", compute="_compute_volume", store=True)
    number_of_transfer = fields.Integer(string="Transfer", compute="_compute_number_of_transfer", store=True)
    number_of_line = fields.Integer(string="Line", compute="_compute_number_of_line", store=True)

    dock_id = fields.Many2one(comodel_name='dock', string="Dock")
    vehicle_id = fields.Many2one(comodel_name='fleet.vehicle', string="Vehicle")
    category_id = fields.Many2one(comodel_name='fleet.vehicle.model.category', string='Category', compute='_compute_category', store=True)

    @api.depends('vehicle_id', 'vehicle_id.category_id')
    def _compute_category(self):
        for record in self:
            record.category_id = record.vehicle_id.category_id.id

    @api.depends('picking_ids', 'picking_ids.move_ids', 'category_id.max_weight', 'picking_ids.move_ids.product_id.weight')
    def _compute_weight_percentage(self):
        for record in self:
            max_weight = record.category_id.max_weight
            total_weight = 0
            for picking_line in record.picking_ids:
                for move_line in picking_line.move_ids:
                    total_weight = total_weight + move_line.product_id.weight * move_line.quantity
            if max_weight == 0:
                record.weight_percentage = 0.0
            else:
                record.weight_percentage = total_weight / max_weight * 100

    @api.depends('picking_ids', 'picking_ids.move_ids', 'category_id.max_volume', 'picking_ids.move_ids.product_id.volume')
    def _compute_volume_percentage(self):
        for record in self:
            max_volume = record.category_id.max_volume
            total_volume = 0
            for picking_line in record.picking_ids:
                for move_line in picking_line.move_ids:
                    total_volume = total_volume + move_line.product_id.volume * move_line.quantity
            if max_volume == 0:
                record.volume_percentage = 0.0
            else:
                record.volume_percentage = total_volume / max_volume * 100
    
    @api.depends('picking_ids', 'picking_ids.move_ids', 'picking_ids.move_ids.product_id.weight')
    def _compute_weight(self):
        for record in self:
            total_weight = 0
            for picking_line in record.picking_ids:
                for move_line in picking_line.move_ids:
                    total_weight = total_weight + move_line.product_id.weight * move_line.quantity
            record.weight = total_weight

    @api.depends('picking_ids', 'picking_ids.move_ids', 'picking_ids.move_ids.product_id.volume')
    def _compute_volume(self):
        for record in self:
            total_volume = 0
            for picking_line in record.picking_ids:
                for move_line in picking_line.move_ids:
                    total_volume = total_volume + move_line.product_id.volume * move_line.quantity
            record.volume = total_volume

    @api.depends('picking_ids')
    def _compute_number_of_transfer(self):
        for record in self:
            record.number_of_transfer = len(record.picking_ids)
    
    @api.depends('picking_ids', 'picking_ids.move_ids')
    def _compute_number_of_line(self):
        for record in self:
            total_lines = 0
            for picking_line in record.picking_ids:
                    total_lines = total_lines + len(picking_line.move_ids)
            record.number_of_line = total_lines
