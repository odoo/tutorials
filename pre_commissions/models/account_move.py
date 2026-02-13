from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        res = super().action_post()
        # breakpoint()
        for move in self:
            if move.move_type != 'out_invoice':
                continue

            sale_orders = move.invoice_line_ids.sale_line_ids.order_id
            sale_orders = sale_orders.exists()

            if not sale_orders:
                continue

            self.env['sale.commission'].sudo().check_commission_rules(sale_orders, move)
        return res
