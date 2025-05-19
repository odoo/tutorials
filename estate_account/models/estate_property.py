from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        """
        Create an invoice for the property sale
        """
        result = super().action_sold()
        if not result:
            return result

        self.env['account.move'].create(
            {
                'move_type': 'out_invoice',
                'partner_id': self.buyer_id.id,
                'invoice_line_ids': [
                    Command.create({'name': self.name, 'quantity': 1, 'price_unit': self.best_price}),
                    Command.create({'name': 'Taxes', 'quantity': 1, 'price_unit': self.best_price * 0.06}),
                    Command.create({'name': 'Adminsitration Fees', 'quantity': 1, 'price_unit': 100}),
                ],
            }
        )
        return result
