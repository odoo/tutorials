from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_set_sold_property(self):

        invoice_value = {
            'partner_id': self.buyer.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    'name': 'Commission (6% of selling price)',
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,
                }),
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100,
                }),
            ]
        }

        self.env['account.move'].create(invoice_value)

        return super().action_set_sold_property()
