from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        account_moves = [self.prepare_account_move(estate) for estate in self]
        self.env['account.move'].create(account_moves)
        return super().action_set_sold()

    def prepare_account_move(self, estate):
        return {
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    'name': estate.name,
                    'quantity': 0.06,
                    'price_unit': estate.selling_price,
                }),
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100,
                }),
            ]
        }
