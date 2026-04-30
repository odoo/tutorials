from odoo import Command, models


class EstateAccount(models.Model):
    _inherit = "estate.property"

    def action_sell(self):
        for property in self:
            partner_id = property.buyer_id.id

            self.env["account.move"].create(
                {
                    "partner_id": partner_id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": property.name,
                                "quantity": 1,
                                "price_unit": property.selling_price * 0.06,
                            }
                        ),
                        Command.create(
                            {
                                "name": "Administrative Fees",
                                "quantity": 1,
                                "price_unit": 100,
                            }
                        ),
                    ],
                }
            )

        return super().action_sell()
