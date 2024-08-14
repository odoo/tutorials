from odoo import Command, models


class InheritedModel(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        self.env["account.move"].create(
            {
                "name": "Test",
                "partner_id": self.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "6% of Selling Price",
                            "quantity": 1,
                            "price_unit": self.selling_price * 0.06,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Administrative Fees",
                            "quantity": 1,
                            "price_unit": 100.00,
                        }
                    ),
                ],
            }
        )
        return super().action_sold()
