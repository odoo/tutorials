# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import AccessError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    is_bulk_return = fields.Boolean(string="Is Bulk Return", copy=False)
    bulk_return_ids = fields.Many2many(comodel_name='stock.picking', relation='stock_picking_stock_picking_bulk_return_rel', column1='picking1', column2='picking2', string='Return of pickings', help="All the return move's pickings", readonly=True, compute='_compute_bulk_return_ids')
    sale_order_ids = fields.Many2many(comodel_name='sale.order', string="Sale Orders", compute='_compute_sale_order_ids')
    purchase_order_ids = fields.Many2many(comodel_name='purchase.order', string="Purchase Orders", compute='_compute_purchase_order_ids')
    credit_note_id = fields.Many2one(comodel_name='account.move', string='Credit Note')
    group_ids = fields.Many2many(comodel_name='procurement.group', string='Procurement Groups')

    @api.depends('move_ids_without_package')
    def _compute_bulk_return_ids(self):
        for picking in self:
            picking.bulk_return_ids = picking.move_ids_without_package.mapped('origin_returned_move_id.picking_id') or False

    @api.depends('move_ids_without_package.sale_line_id')
    def _compute_sale_order_ids(self):
        for picking in self:
            picking.sale_order_ids = picking.move_ids_without_package.mapped('sale_line_id.order_id')

    @api.depends('move_ids_without_package.purchase_line_id')
    def _compute_purchase_order_ids(self):
        for picking in self:
            picking.purchase_order_ids = picking.move_ids_without_package.mapped('purchase_line_id.order_id')

    def action_create_credit_note(self):
        if not self.env.user.has_group('account.group_account_manager'):
            raise AccessError(_("Only account manager can create credit note."))
        notifications = []
        for picking in self:
            to_invoice_line_ids = []
            for move in picking.move_ids_without_package:
                order_line = move.sale_line_id or move.purchase_line_id
                if order_line.qty_invoiced < move.product_uom_qty:
                    order_line.qty_to_invoice = -order_line.qty_invoiced
                    notifications.append(order_line.order_id)
                else:
                    order_line.qty_to_invoice = -move.product_uom_qty
                to_invoice_line_ids.append(order_line.id)
            if picking.sale_order_ids:
                picking.credit_note_id = picking.sale_order_ids.with_context({'to_invoice_line_ids': to_invoice_line_ids})._create_invoices(final=True)
            elif picking.purchase_order_ids:
                picking.credit_note_id = picking.purchase_order_ids.with_context({'to_invoice_line_ids': to_invoice_line_ids}).action_create_invoice().get('res_id')

        if notifications:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _("Check credit note"),
                    'message': _("Following orders contained lines whose invoiced quantity was less than the returned quantity. %s" % ', '.join([order.name for order in notifications])),
                    'type': 'warning',
                    'sticky': True,
                    'next': {'type': 'ir.actions.act_window_close'},
                }
            }

    def action_view_source_pickings(self):
        self.ensure_one()
        return {
            'name': _("Source Pickings"),
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'stock.picking',
            'domain': [('id', 'in', self.bulk_return_ids.ids)],
        }

    def action_view_sale_orders(self):
        self.ensure_one()
        return {
            'name': _("Sale Orders"),
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'sale.order',
            'domain': [('id', 'in', self.sale_order_ids.ids)],
        }

    def action_view_purchase_orders(self):
        self.ensure_one()
        return {
            'name': _("Purchase Orders"),
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'purchase.order',
            'domain': [('id', 'in', self.purchase_order_ids.ids)],
        }

    def action_view_credit_note(self):
        self.ensure_one()
        return {
            'name': _("Credit Note"),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': self.credit_note_id.id,
        }
