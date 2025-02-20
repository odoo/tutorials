from odoo import models, Command


class Property(models.Model):
    _inherit = "estate.property"

    def action_mark_sold(self):
        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            # 'journal_id': ,
            'invoice_line_ids': [
                Command.create({
                    'name': "6%",
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,
                }),
                Command.create({
                    'name': "Administrative Fees",
                    'quantity': 1,
                    'price_unit': 100.00,
                }),
            ]
        })
        return super().action_mark_sold()
