from odoo import Command, models


class Properties(models.Model):
    _inherit = ["estate.property"]
    _name = "estate.property"

    def action_sold(self):
        self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.buyer_id.id,
                "journal_id": 1,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "Taxes",
                            "quantity": 1,
                            "price_unit": (6 / 100) * self.selling_price,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Administrative fees",
                            "quantity": 1,
                            "price_unit": 100.00,
                        }
                    ),
                ],
            }
        )
        return super().action_sold()
