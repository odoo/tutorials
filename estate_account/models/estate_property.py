from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        self.env["account.move"].create({
            "partner_id": self.buyer.id,
            "move_type": "out_invoice",
            "journal_id": 1,
            "line_ids": [
                Command.create({
                    "name": self.name,
                    "quantity": 1.0,
                    "price_unit": 0.06 * self.selling_price
                }),
                Command.create({
                    "name": "Administrative fees",
                    "quantity": 1.0,
                    "price_unit": 100.0
                })
            ],
        })
        return super().action_sold()
