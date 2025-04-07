# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    all_picking_ids = fields.Many2many(comodel_name='stock.picking', string='Deliveries & Returns', compute='_compute_all_picking_ids')

    @api.depends('order_line.move_ids')
    def _compute_all_picking_ids(self):
        for order in self:
            order.all_picking_ids = [Command.link(picking.id) for picking in order.order_line.mapped('move_ids.picking_id')]

    @api.depends('all_picking_ids')
    def _compute_picking_ids(self):
        for order in self:
            order.delivery_count = len(order.all_picking_ids)

    def _get_action_view_picking(self, pickings):
        return super()._get_action_view_picking(self.all_picking_ids)

    def _get_invoiceable_lines(self, final=False):
        invoiceable_lines = super()._get_invoiceable_lines(final=final)
        if self.env.context.get('to_invoice_line_ids'):
            invoiceable_lines = invoiceable_lines.filtered(lambda line: line.id in self.env.context.get('to_invoice_line_ids'))
        return invoiceable_lines
