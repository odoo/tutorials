from odoo import models, Command, fields


class EstateAccount(models.Model):
    _inherit = "estate.property"

    def action_to_sold(self):
        self.env["account.move"].create(
            {
                "partner_id": self.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_date": fields.Date.today(),
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": self.name,
                            "quantity": 1,
                            "price_unit": self.expected_price,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Additional Charges",
                            "quantity": 1,
                            "price_unit": self.expected_price * 0.06,
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
        return super().action_to_sold()
