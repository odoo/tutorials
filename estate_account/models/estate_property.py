from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        print(" reached ".center(100, "="))
        self.check_access("write")
        invoice = (
            self.sudo()
            .env["account.move"]
            .create(
                {
                    "partner_id": self.buyer_id.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": self.name,
                                "quantity": 1,
                                "price_unit": 0.06 * self.selling_price,
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
                },
            )
        )

        return super().action_sold()
