from odoo import models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_set_sold(self):
        # print("Overridden action_set_sold method in estate_account")
        move_values = {
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
               # 6% of the selling price
                (0, 0, {
                    'name': 'Commission (6% of selling price)',
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,
                }),
                # Administrative fees of 100.00
                (0, 0, {
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100.00,
                }),
            ],
            }
        self.env['account.move'].create(move_values)
        # print(f"Created account.move with ID: {account_move.id} and invoice lines")
        return super().action_set_sold()
