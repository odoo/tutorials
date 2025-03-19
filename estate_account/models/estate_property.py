from odoo import models, Command

class Property(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        self.env["account.move"].create({
            "move_type": "out_invoice",
            "journal_id": journal.id,
            "partner_id": self.buyer_id.id,
            "name": self.name,
            "line_ids": [
                Command.create({
                    "name": "6% of the price",
                    "quantity": 1,
                    "price_unit": 0.06 * self.selling_price
                }),
                Command.create({
                    "name": "Administrative fees",
                    "quantity": 1,
                    "price_unit": 100.00
                })
            ]
        })
        return super().action_set_sold()
