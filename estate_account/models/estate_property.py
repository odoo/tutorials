from odoo import models, Command


class EstateProperty(models.Model):
    _name = "estate.property"
    _inherit = "estate.property"

    def sell_property(self):
        self.env['account.move'].create(
            {
                'partner_id': self.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': 'Selling Price',
                        'quantity': '1',
                        'price_unit': self.selling_price * 0.06
                    }),
                    Command.create({
                        'name': 'Administrative Fees',
                        'quantity': '1',
                        'price_unit': 100.00
                    })
                ]
            }
        )
        return super().sell_property()
