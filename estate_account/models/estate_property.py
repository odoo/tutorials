from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold_property(self):
        invoice_vals = {
            "name": "INV° " + str(self.id),
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            "line_ids": [
                Command.create({
                    "name": "6% of the selling price",
                    "quantity": "1",
                    "price_unit": self.selling_price * 0.06,
                }),
                Command.create({
                    "name": "administrative fees",
                    "quantity": 1,
                    "price_unit": 100.00,
                })
            ],
        }
        self.env['account.move'].create(invoice_vals)
        return super().action_sold_property()
