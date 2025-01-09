from odoo import models,Command
from datetime import datetime


class Property_Invoice(models.Model):
    _inherit = "test.property"

    def action_sold(self):
        self.env["account.move"].create(
                {
                    "partner_id":self.buyer_id.id,
                    "move_type": "out_invoice",
                    'invoice_line_ids': [
                Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price,
                                  }),

                Command.create({
                    'name': "tax 6%",
                    'quantity': 1,
                    'price_unit': self.selling_price*0.06
                               }),

                Command.create({
                    'name': "administrative fees",
                    'quantity': 1,
                    'price_unit': 100.00
                               })
            ]


           }

        ).action_post()
        return super().action_sold()

