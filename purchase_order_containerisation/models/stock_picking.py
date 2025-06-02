# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    lifecycle_status = fields.Selection([
        ('in_production', 'In Production'),
        ('containerised', 'Containerised'),
        ('on_water', 'On Water'),
        ('customs', 'Customs'),
        ('booked_in', 'Booked In')
    ], string='Lifecycle Status', default='in_production', readonly=True)
    vessel_tracking = fields.Char(string='Vessel Tracking')
    source_transfers = fields.Char(string='Source Transfers')
    is_container_picking = fields.Boolean(compute='_compute_is_container_picking', string='Container Transfer', store=True)

    @api.depends('picking_type_id')
    def _compute_is_container_picking(self):
        for record in self:
            record.is_container_picking = (
                record.picking_type_id and record.picking_type_id.sequence_code == "IN/CONT"
            )

    @api.model_create_multi
    def create(self, vals_list):
        pickings = super().create(vals_list)
        for picking in pickings:
            if picking.backorder_id:
                picking.lifecycle_status = 'booked_in'
        return pickings

    def write(self, vals):
        if isinstance(vals, list):
            vals = vals[0]
        lifecycle_status = vals.get('lifecycle_status', False)
        for record in self:
            if 'backorder_id' in vals and record.backorder_id:
                record.lifecycle_status = 'customs'
        if lifecycle_status == 'containerised':
            for picking in self:
                for move in picking.move_ids:
                    original_move = move.move_orig_ids
                    if original_move:
                        containerised_qty = move.quantity_to_containerise
                        remaining_qty = original_move.product_uom_qty - containerised_qty
                        original_move.write({'product_uom_qty': remaining_qty})
                        move.write({'product_uom_qty': containerised_qty, 'quantity': containerised_qty})
                        if remaining_qty == 0:
                            original_move.write({'state': 'cancel'})
        return super().write(vals)

    def button_containerise(self):
        self.lifecycle_status = 'containerised'
        self.state = 'assigned'

    def button_on_water(self):
        if not self.vessel_tracking:
            raise UserError(_("Please enter tracking details before moving to On The Water."))
        self.lifecycle_status = 'on_water'

    def button_at_custom(self):
        self.lifecycle_status = 'customs'

    def button_validate(self):
        res = super().button_validate()
        for record in self:
            if record.is_container_picking:
                backorder = self.env['stock.picking'].search([('backorder_id', '=', record.id)], limit=1)
                if backorder:
                    backorder.lifecycle_status = 'customs'

                if record.lifecycle_status == 'in_production':
                    record.button_containerise()
                    record.button_on_water()
                    record.button_at_custom()
                    record.button_validate()
                elif record.lifecycle_status == 'containerised':
                    record.button_on_water()
                elif record.lifecycle_status == 'on_water':
                    record.lifecycle_status = 'customs'

                if record.state == 'done':
                    record.lifecycle_status = 'booked_in'
        return res

    def action_assign(self):
        for record in self:
            if record.state == 'draft':
                record.lifecycle_status = 'containerised'
        return super().action_assign()
