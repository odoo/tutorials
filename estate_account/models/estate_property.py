from odoo import models, Command


class EstateProperty(models.Model):

    _inherit = "estate.property"

    def action_sold(self):
        super().action_sold()
        move_values = {
            "partner_id": self.buyer.id,
            "move_type": "out_invoice",
            "invoice_line_ids": [
                Command.create({
                    "name": "6% of selling price",
                    "quantity": 1,
                    "price_unit": 0.6 * self.selling_price
                }),
                Command.create({
                    "name": "administrative fees",
                    "quantity": 1,
                    "price_unit": 100.0
                })
            ],
        }
        self.env['account.move'].create(move_values)
