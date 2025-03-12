# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import _, Command, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import groupby


class StockBulkReturn(models.TransientModel):
    _name = 'stock.bulk.return'
    _description = "Stock Bulk Return"
    _inherit = 'barcodes.barcode_events_mixin'

    picking_type_code = fields.Selection(related='picking_type_id.code')
    date_order_after = fields.Date(string="Orders After", required=True, default=lambda self: datetime.now().date() - relativedelta(months=12))
    date_picking_after = fields.Date(string="Pickings After", required=True, default=lambda self: datetime.now().date() - relativedelta(months=12))

    picking_type_id = fields.Many2one(comodel_name='stock.picking.type', string="Operation Type", required=True, domain=[
        ('code', 'in', ['incoming', 'outgoing']),
    ])
    partner_id = fields.Many2one(comodel_name='res.partner', string="Customer/Vendor", required=True)
    location_src_id = fields.Many2one(comodel_name='stock.location', string="Source Location", readonly=False, store=True, compute='_compute_location_src_id')
    location_dest_id = fields.Many2one(comodel_name='stock.location', string="Destination Location", readonly=False, store=True, compute='_compute_location_dest_id')
    bulk_return_line_ids = fields.One2many(comodel_name='stock.bulk.return.line', inverse_name='bulk_return_id', string="Return Lines", required=True)

    @api.depends('picking_type_id', 'partner_id')
    def _compute_location_src_id(self):
        customer_loc, supplier_loc = self.env['stock.warehouse']._get_partner_locations()
        for wizard in self:
            wizard.location_src_id = customer_loc.id
            if wizard.picking_type_id:
                self.location_src_id = wizard.picking_type_id.return_picking_type_id.default_location_dest_id.id
                if self.location_src_id.usage == 'customer' and wizard.partner_id and wizard.partner_id.property_stock_customer:
                    self.location_src_id = wizard.partner_id.property_stock_customer.id

    @api.depends('picking_type_id', 'partner_id')
    def _compute_location_dest_id(self):
        customer_loc, supplier_loc = self.env['stock.warehouse']._get_partner_locations()
        for wizard in self:
            wizard.location_dest_id = supplier_loc.id
            if wizard.picking_type_id:
                self.location_dest_id = wizard.picking_type_id.return_picking_type_id.default_location_src_id.id
                if self.location_dest_id.usage == 'supplier' and wizard.partner_id and wizard.partner_id.property_stock_supplier:
                    self.location_dest_id = wizard.partner_id.property_stock_supplier.id

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id:
            self.bulk_return_line_ids = False

    @api.onchange('picking_type_id')
    def onchange_picking_type_id(self):
        if self.picking_type_id:
            self.bulk_return_line_ids = False

    @api.onchange('date_order_after')
    def onchange_date_order_after(self):
        if self.date_order_after and self.bulk_return_line_ids:
            if self.picking_type_code == 'incoming':
                self.bulk_return_line_ids = [Command.unlink(line.id) for line in self.bulk_return_line_ids if (line.sale_order_id and line.sale_order_id.date_order.date() < self.date_order_after)]
            elif self.picking_type_code == 'outgoing':
                self.bulk_return_line_ids = [Command.unlink(line.id) for line in self.bulk_return_line_ids if (line.purchase_order_id and line.purchase_order_id.date_order.date() < self.date_order_after)]

    @api.onchange('date_picking_after')
    def onchange_date_picking_after(self):
        if self.date_picking_after and self.bulk_return_line_ids:
            self.bulk_return_line_ids = [Command.unlink(line.id) for line in self.bulk_return_line_ids if (line.picking_id and line.picking_id.date_done and line.picking_id.date_done.date() < self.date_picking_after)]

    def on_barcode_scanned(self, barcode):
        if not barcode:
            return
        barcode = barcode.strip()
        new_lines = []

        if picking_type := self.env['stock.picking.type'].search([('barcode', '=', barcode)], limit=1):
            if not self.picking_type_id or picking_type != self.picking_type_id:
                self.picking_type_id = picking_type.id
        elif picking := self.env['stock.picking'].search([('name', '=', barcode)], limit=1):
            if not self.partner_id:
                self.partner_id = picking.partner_id.id
            if picking.partner_id != self.partner_id:
                raise UserError(_("Partner in this picking does not match the selected partner."))
            elif picking.picking_type_code in ['internal', self.picking_type_code]:
                raise UserError(_("Picking operation type cannot be internal or same as selected operation type."))
            elif picking.state != 'done':
                raise UserError(_("Return can only be created of Done pickings."))
            elif picking.date_done.date() < self.date_picking_after:
                raise UserError(_("Delivery date is before the selected date."))
            elif picking.sale_id and self.date_order_after and picking.sale_id.date_order.date() < self.date_order_after:
                raise UserError(_("Order date is before the selected date."))
            elif picking.purchase_id and self.date_order_after and picking.purchase_id.date_order.date() < self.date_order_after:
                raise UserError(_("Order date is before the selected date."))

            for move in picking.move_ids_without_package:
                if move.lot_ids:
                    for lot in move.lot_ids.filtered(lambda lot: lot.id not in self.bulk_return_line_ids.filtered(lambda line: line.move_id == move).mapped('lot_id.id')):
                        new_lines.append({
                            'product_id': move.product_id.id,
                            'lot_id': lot.id,
                            'picking_id': picking.id,
                        })
                elif move.id not in self.bulk_return_line_ids.mapped('move_id.id'):
                    new_lines.append({
                        'product_id': move.product_id.id,
                        'picking_id': picking.id,
                    })
        elif not self.partner_id:
            raise UserError(_("Please select a partner first."))
        elif lots := self.env['stock.lot'].search([('name', '=', barcode)]):
            move_lines = self.env['stock.move.line'].search([
                ('move_id.picking_id.state', '=', 'done'),
                ('move_id.picking_id.picking_type_code', 'not in', ['internal', self.picking_type_code]),
                ('move_id.partner_id', '=', self.partner_id.id),
                ('lot_id', 'in', lots.ids),
            ])
            if not move_lines:
                raise UserError(_("Either the pickings aren't in validated or no product from this lot was sold to/purchased from selected partner."))
            moves = list(set(move_lines.mapped('move_id')))
            for move in moves:
                lot = lots.filtered(lambda lot: lot.product_id == move.product_id)
                if not self.bulk_return_line_ids.filtered(lambda line: line.move_id == move and line.lot_id == lot):
                    new_lines.append({
                        'product_id': move.product_id.id,
                        'lot_id': lot.id,
                        'picking_id': move.picking_id.id,
                    })
        elif product := self.env['product.product'].search([('barcode', '=', barcode)], limit=1):
            domain = [
                ('product_id', '=', product.id),
                ('picking_id.state', '=', 'done'),
                ('picking_id.partner_id', '=', self.partner_id.id),
                ('picking_id.picking_type_code', 'not in', ['internal', self.picking_type_code]),
                ('picking_id.date_done', '>=', self.date_picking_after),
            ]
            if self.picking_type_code == 'incoming':
                domain.append(('sale_line_id.order_id.date_order', '>=', self.date_order_after))
            elif self.picking_type_code == 'outgoing':
                domain.append(('purchase_line_id.order_id.date_order', '>=', self.date_order_after))
            moves = self.env['stock.move'].search(domain)
            if not moves:
                raise UserError(_("Either picking not Done or partner not same or product not delivered to/received from this partner or dates don't match."))
            for move in moves:
                if not self.bulk_return_line_ids.filtered(lambda line: line.move_id == move):
                    new_lines.append({
                        'product_id': product.id,
                        'picking_id': move.picking_id.id,
                    })
        else:
            raise UserError(_("No operation, delivery, receipt, lot, serial, product found corresponding to barcode %s", barcode))

        if new_lines:
            self.bulk_return_line_ids = [Command.create(line) for line in new_lines]

    def _prepare_move_vals(self, wizard):
        move_vals = []

        for move, lines in groupby(wizard.bulk_return_line_ids, lambda line: line.move_id):
            move_orig_to_link = move.move_dest_ids.returned_move_ids
            move_orig_to_link |= move
            move_orig_to_link |= move.move_dest_ids.filtered(lambda m: m.state not in ('cancel')).move_orig_ids.filtered(lambda m: m.state not in ('cancel'))
            move_dest_to_link = move.move_orig_ids.returned_move_ids
            move_dest_to_link |= move.move_orig_ids.returned_move_ids.move_orig_ids.filtered(lambda m: m.state not in ('cancel')).move_dest_ids.filtered(lambda m: m.state not in ('cancel'))

            line_vals = []
            for line in lines:
                line_val = {
                    'picking_id': line.picking_id.id,
                    'product_id': line.product_id.id,
                    'quantity': line.return_qty,
                }
                if line.lot_id:
                    line_val.update({
                        'lot_id': line.lot_id.id,
                    })
                line_vals.append(line_val)
            move_val = {
                'origin': move.sale_line_id.order_id.name or move.purchase_line_id.order_id.name,
                'name': move.picking_id.name,
                'product_id': move.product_id.id,
                'product_uom_qty': sum(line.return_qty for line in lines),
                'product_uom': move.product_id.uom_id.id,
                'state': 'draft',
                'to_refund': True,
                'location_id': wizard.location_src_id.id,
                'location_dest_id': wizard.location_dest_id.id,
                'origin_returned_move_id': move.id,
                'move_orig_ids': [Command.link(m.id) for m in move_orig_to_link],
                'move_dest_ids': [Command.link(m.id) for m in move_dest_to_link],
                'procure_method': 'make_to_stock',
                'group_id': move.picking_id.group_id.id,
                'move_line_ids': [Command.create(line_val) for line_val in line_vals],
            }
            if wizard.picking_type_code == 'incoming':
                move_val.update({
                    'sale_line_id': move.sale_line_id.id,
                })
            elif wizard.picking_type_code == 'outgoing':
                move_val.update({
                    'partner_id': wizard.partner_id.id,
                    'purchase_line_id': move.purchase_line_id.id
                })
            move_vals.append(move_val)
        return move_vals

    def _prepare_picking_vals(self, wizard, move_vals):
        return {
            'origin': _("Return of %s", ', '.join(wizard.bulk_return_line_ids.mapped('picking_id.name'))),
            'state': 'draft',
            'partner_id': wizard.partner_id.id,
            'picking_type_id': wizard.picking_type_id.id,
            'location_id': wizard.location_src_id.id,
            'location_dest_id': wizard.location_dest_id.id,
            'move_ids_without_package': [Command.create(move) for move in move_vals],
            'is_bulk_return': True,
        }

    def _action_confirm(self):
        picking_vals = []
        for wizard in self:
            if not wizard.bulk_return_line_ids or not wizard.bulk_return_line_ids.mapped('move_id'):
                raise UserError(_("No returns added."))
            move_vals = self._prepare_move_vals(wizard)
            picking_val = self._prepare_picking_vals(wizard, move_vals)
            picking_vals.append(picking_val)
        return self.env['stock.picking'].create(picking_vals)

    def action_confirm(self):
        self.ensure_one()
        bulk_return_picking = self._action_confirm()
        return {
            'name': _("Bulk Return Picking"),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'res_id': bulk_return_picking.id,
        }
