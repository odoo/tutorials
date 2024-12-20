
from odoo import Command, models

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_state_sold(self):
        self.ensure_one()
        self.env["account.move"].create({
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "invoice_line_ids": [
                Command.create({
                    "name": "Property",
                    "quantity": 1.0,
                    "price_unit": self.selling_price * 0.06
                }),
                Command.create({
                    "name": "Administrative fees",
                    "quantity": 1.0,
                    "price_unit": 100000.0
                })
            ]
        })
        return super().action_set_state_sold()

