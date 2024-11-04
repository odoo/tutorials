from odoo import fields, models, api


class stockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'

    weight = fields.Float(compute="_compute_weight", string='Weight')
    volume = fields.Float(compute="_compute_volume", string='Volume')

    dock_id = fields.Many2one(comodel_name='dock', string="Dock")
    vehicle_id = fields.Many2one(comodel_name='fleet.vehicle', string="Vehicle")
    category_id = fields.Many2one(comodel_name='fleet.vehicle.model.category', string='Category', compute='_compute_category')

    @api.depends('vehicle_id')
    def _compute_category(self):
        for record in self:
            record.category_id = record.vehicle_id.category_id.id

    def _compute_weight(self):
        for record in self:
            max_weight = record.category_id.max_weight
            for picking_line in record.picking_ids:
                for move_line in picking_line.move_ids:
                    record.weight = record.weight + move_line.product_id.weight * move_line.quantity
            total_weight = record.weight
            if max_weight == 0:
                record.weight = 0.0
            else:
                record.weight = total_weight / max_weight * 100

    def _compute_volume(self):
        for record in self:
            max_volume = record.category_id.max_volume
            for picking_line in record.picking_ids:
                for move_line in picking_line.move_ids:
                    record.volume = record.volume + move_line.product_id.volume * move_line.quantity
            if max_volume == 0:
                record.volume = 0.0
            else:
                record.volume = record.volume / max_volume * 100
        