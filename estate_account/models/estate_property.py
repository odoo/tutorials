from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    # Extended method for Sold button action
    def action_set_sold(self):
        # Compute amounts
        commission = self.selling_price * 0.06  # 6% of selling price
        admin_fee = 100.0

        invoice_vals = {
            'partner_id': self.partner_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    'name': 'Commission (6% of selling price)',
                    'quantity': 1,
                    'price_unit': commission,
                }),
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': admin_fee,
                }),
            ]
        }

        self.env['account.move'].create(invoice_vals)

        return super().action_set_sold()
