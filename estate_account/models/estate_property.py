from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sell(self):
        self.env['account.move'].create(
            {
                'move_type': 'out_invoice',
                'partner_id': self.partner_id.id,
                'invoice_line_ids': [
                    Command.create({'name': self.name, 'quantity': 1, 'price_unit': self.best_offer}),
                    Command.create({'name': 'Taxes', 'quantity': 1, 'price_unit': self.best_offer * 0.06}),
                    Command.create({'name': 'Adminsitration Fees', 'quantity': 1, 'price_unit': 100}),
                ],
            }
        )
        return super().action_sell()
