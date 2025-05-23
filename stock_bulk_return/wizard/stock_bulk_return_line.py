# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockBulkReturnLine(models.TransientModel):
    _name = 'stock.bulk.return.line'
    _description = "Stock Bulk Return Line"
    _rec_name = 'product_id'
    _order = 'bulk_return_id, product_id, lot_id, picking_id, move_id, id'
    _sql_constraints = [
        ('move_lot_uniq', "UNIQUE(bulk_return_id, move_id, lot_id)", "Combination of stock move and stock lot must be unique."),
        ('check_max_return_qty', "CHECK(max_return_qty > 0)", "There is no quantity to return."),
        ('check_return_qty', "CHECK(return_qty > 0 AND return_qty <= max_return_qty)", "Return quantity must be positive and less than or equal to maximum return quantity."),
    ]

    return_qty = fields.Float(string="Return Quantity", digits='Product Unit of Measure', required=True, default=1.0)

    bulk_return_id = fields.Many2one(comodel_name='stock.bulk.return', required=True, ondelete='cascade')
    product_id = fields.Many2one(comodel_name='product.product', string="Product", required=True, domain=[('type', '=', 'consu')])
    lot_id = fields.Many2one(comodel_name='stock.lot', string="Lot/Serial No.")
    picking_id = fields.Many2one(comodel_name='stock.picking', string="Delivery/Receipt", required=True)

    product_tracking = fields.Selection(related='product_id.tracking', string='Tracking')
    uom_id = fields.Many2one(related='product_id.uom_id', string='Unit of Measure')
    move_id = fields.Many2one(comodel_name='stock.move', string="Stock Move", store=True, compute='_compute_move_id')
    max_return_qty = fields.Float(string="Max Return Quantity", help="Maximum quantity that can be returned", store=True, compute='_compute_max_return_qty')
    sale_order_id = fields.Many2one(related='move_id.sale_line_id.order_id', string="Sale Order")
    purchase_order_id = fields.Many2one(related='move_id.purchase_line_id.order_id', string="Purchase Order")

    @api.depends('bulk_return_id', 'product_id', 'lot_id', 'picking_id')
    def _compute_move_id(self):
        for line in self:
            line.move_id = False
            if not line.product_id or not line.picking_id or line.picking_id.state != 'done' or line.picking_id.return_id or line.picking_id.bulk_return_ids:
                continue
            moves = line.picking_id.move_ids_without_package.filtered(lambda m: m.product_id == line.product_id)
            if not moves:
                continue
            if line.product_id.tracking in ['lot', 'serial']:
                if line.lot_id:
                    moves = moves.filtered(lambda move: line.lot_id.id in move.lot_ids.ids and 
                        move.id not in line.bulk_return_id.bulk_return_line_ids.filtered(lambda brl: brl.lot_id == line.lot_id).mapped('move_id.id'))
                else:
                    moves = []
            else:
                moves = moves.filtered(lambda m: m.id not in line.bulk_return_id.bulk_return_line_ids.mapped('move_id.id'))
            line.move_id = moves[:1]

    @api.depends('move_id')
    def _compute_max_return_qty(self):
        """
        Compute the maximum quantity that can be returned for a stock move
        - For Sale Orders:
        Any returned quantity from incoming pickings moves that is a return of this move is deducted from the total delivered quantity from selected outgoing picking.
        - For Purchase Orders:
        Any returned quantity from outgoing pickings moves that is a return of this move is deducted from the total received quantity from selected incoming picking.
        """
        for line in self:
            if line.sale_order_id:
                move_lines = line.move_id.sale_line_id.move_ids.filtered(lambda move: move.state == 'done' and move.picking_id.state == 'done').mapped('move_line_ids')
                if line.lot_id:
                    move_lines = move_lines.filtered(lambda ml: ml.lot_id == line.lot_id)
                outgoing_qty = sum(move_lines.filtered(lambda ml: ml.picking_code == 'outgoing' and ml.picking_id == line.picking_id).mapped('quantity'))
                incoming_qty = sum(move_lines.filtered(lambda ml: ml.picking_code == 'incoming' and ml.move_id.origin_returned_move_id == line.move_id).mapped('quantity'))
                line.max_return_qty = outgoing_qty - incoming_qty
            elif line.purchase_order_id:
                move_lines = line.move_id.purchase_line_id.move_ids.mapped('move_line_ids')
                if line.lot_id:
                    move_lines = move_lines.filtered(lambda ml: ml.lot_id == line.lot_id)
                incoming_qty = sum(move_lines.filtered(lambda ml: ml.picking_code == 'incoming' and ml.picking_id == line.picking_id).mapped('quantity'))
                outgoing_qty = sum(move_lines.filtered(lambda ml: ml.picking_code == 'outgoing' and ml.move_id.origin_returned_move_id == line.move_id).mapped('quantity'))
                line.max_return_qty = incoming_qty - outgoing_qty
            else:
                line.max_return_qty = False

    @api.constrains('max_return_qty')
    def _check_lot_id(self):
        if self.filtered(lambda line: line.lot_id and line.move_id and line.lot_id.id not in line.move_id.lot_ids.ids):
            raise ValidationError(_("Lot/Serial No. must be in the selected move."))

    @api.constrains('product_id', 'lot_id')
    def _check_product_lot(self):
        if self.filtered(lambda line: line.product_id and line.lot_id and line.lot_id.product_id != line.product_id):
            raise ValidationError(_("Lot/Serial No. must belong to the selected product."))

    @api.constrains('product_id', 'picking_id')
    def _check_product_picking(self):
        if self.filtered(lambda line: line.product_id and line.picking_id and line.product_id.id not in line.picking_id.move_ids_without_package.mapped('product_id.id')):
            raise ValidationError(_("Product must be moved in the selected picking."))

    @api.constrains('picking_id')
    def _check_picking_id(self):
        for line in self:
            if line.picking_id.state != 'done':
                raise ValidationError(_("You may only return Done pickings."))
            if line.picking_id.return_id or line.picking_id.bulk_return_ids:
                raise ValidationError(_("Picking is already a return."))
            if line.picking_id.partner_id != line.bulk_return_id.partner_id:
                raise ValidationError(_("Picking must belong to the same partner as the bulk return."))
            if line.picking_id.picking_type_code not in ['incoming', 'outgoing']:
                raise ValidationError(_("Picking must be of type Delivery or Receipt."))
            if line.picking_id.picking_type_code == line.bulk_return_id.picking_type_code:
                raise ValidationError(_("Picking must be of opposite type as the bulk return."))

    @api.constrains('product_id', 'sale_order_id', 'purchase_order_id')
    def _check_product_order(self):
        for line in self:
            if line.product_id and line.sale_order_id and line.product_id.id not in line.sale_order_id.order_line.product_id.ids:
                raise ValidationError(_("Product must have a line in selected sale order."))
            if line.product_id and line.purchase_order_id and line.product_id.id not in line.purchase_order_id.order_line.mapped('product_id.id'):
                raise ValidationError(_("Product must have a line in selected purchase order."))

    @api.constrains('lot_id')
    def _check_lot_id(self):
        if self.filtered(lambda line: line.lot_id and line.move_id and line.lot_id.id not in line.move_id.lot_ids.ids):
            raise ValidationError(_("Lot/Serial No. must be in the selected move."))
