# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    origin_returned_picking_id = fields.Many2one(related='origin_returned_move_id.picking_id', string='Origin Returned Picking')
    sale_order_id = fields.Many2one(related='sale_line_id.order_id', string='Sale Order')
    purchase_order_id = fields.Many2one(related='purchase_line_id.order_id', string='Purchase Order')
