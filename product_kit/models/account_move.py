from odoo import models, fields


class AccountMove(models.Model):
    _inherit = "account.move"

    sale_id = fields.Many2one('sale.order', string="Sale Order", compute='_compute_sale_id', store=True, readonly=True)
    print_kit = fields.Boolean(related="sale_id.print_kit", readonly=True)
    from_wizard = fields.Boolean(related="line_ids.sale_line_ids.from_wizard", store=True, readonly=True)

    def _compute_sale_id(self):
        for move in self:
            sale_orders = move.line_ids.mapped("sale_line_ids.order_id")
            move.sale_id = sale_orders and sale_orders[0] or False
