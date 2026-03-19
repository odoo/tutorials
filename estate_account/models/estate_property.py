from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        self.env['account.move'].create(
            {
                'move_type': 'out_invoice',
                'partner_id': self.buyer_id.id,
                'invoice_line_ids': [
                    Command.create(
                        {
                            'name': 'Down Payment',
                            'quantity': 1,
                            'price_unit': self.selling_price * 0.06,
                        }
                    ),
                    Command.create(
                        {
                            'name': 'Administrative Fees',
                            'quantity': 1,
                            'price_unit': 100.00,
                        }
                    ),
                ],
            }
        )
        res = super().action_sold()
        return res

    def _create_invoices(self):
        pass
