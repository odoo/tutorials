from odoo import models, Command


class EstateAccount(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        self.env["account.move"].create({
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "invoice_line_ids": [
                Command.create({
                    "name": "Property Sale Commission",
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06
                }),
                Command.create({
                    "name": "Additional Fees",
                    "quantity": 1,
                    "price_unit": 100.00

                })
            ],
        })

        return super().action_sold()
