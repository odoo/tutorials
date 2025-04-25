from odoo import Command, models
 
class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        self.env['account.move'].create({
            'partner_id': self.buyer.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    "name": "Selling price (6%)",
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.6,
                }),
                Command.create({
                    "name": "Administrative fees",
                    "quantity": 1,
                    "price_unit": 100_000,
                })
            ]
        })
        return super().action_sold()