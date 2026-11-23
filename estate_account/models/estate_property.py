from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = ["estate.property"]

    def action_sold(self):
        self.env["account.move"].create({
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "invoice_line_ids": [
                Command.create({
                    "name": self.name,
                    "quantity": "1",
                    "price_unit": self.selling_price / 100 * 6
                }),
                Command.create({
                    "name": "Administartive fee",
                    "quantity": "1",
                    "price_unit": 100
                })
            ]
        })
        return super().action_sold()
