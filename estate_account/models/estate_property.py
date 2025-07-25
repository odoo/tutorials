from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sell_property(self):
        res = super().sell_property()
        self.env["account.move"].create(
            [
                {
                    "move_type": "out_invoice",
                    "partner_id": self.partner_id.id,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "Deposit",
                                "quantity": 1,
                                "price_unit": self.selling_price * 0.06,
                            }
                        ),
                        Command.create(
                            {
                                "name": "Administrative Fees",
                                "quantity": 1,
                                "price_unit": 100.0,
                            }
                        ),
                    ],
                }
            ]
        )
        return res
