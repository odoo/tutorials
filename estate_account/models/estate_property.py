from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        res = super().action_sold()
        self.env['account.move'].create({
            "move_type": 'out_invoice',
            "partner_id": self.buyer.id,
            "line_ids": [
                Command.create({
                    "name": "6% Fee",
                    "quantity": 1,
                    "price_unit": 0.06 * self.selling_price,
                }),
                Command.create({
                    "name": "Administrative Fee",
                    "quantity": 1,
                    "price_unit": 100,
                }),
            ]
        })
        return res
