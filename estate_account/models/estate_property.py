from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_button(self):
        super().action_sold_button()
        move_vals = {
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                "name": "6% selling price",
                "quantity": 1,
                "price_unit": self.selling_price * 0.6
            }),
                Command.create({
                    "name": "Administration fee",
                    "quantity": 1,
                    "price_unit": 100
                })
            ]
        }
        self.env['account.move'].create(move_vals)
