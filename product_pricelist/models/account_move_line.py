from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    book_price = fields.Float(string="Book Price", compute='_compute_book_price')

    @api.depends('product_id', 'quantity', 'move_id.invoice_origin')
    def _compute_book_price(self):
        sale_orders = {so.name: so for so in self.env['sale.order'].search([('name', 'in', self.mapped('move_id.invoice_origin'))])}
        for record in self:
            if not record.product_id:
                record.book_price = 0.0
                continue

            sale_order = sale_orders.get(record.move_id.invoice_origin)
            if sale_order:
                record.book_price = sale_order.pricelist_id._get_product_price(
                    record.product_id, record.quantity
                ) * record.quantity
            else:
                record.book_price = record.product_id.lst_price * record.quantity
