from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_on_sold_button(self):
        res = super().action_on_sold_button()
        self.env["account.move"].create(
            {
                "partner_id": self.buyer.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "6% of the selling price",
                            "quantity": 1,
                            "price_unit": self.selling_price * 0.06,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Administrative fees",
                            "quantity": 1,
                            "price_unit": 100,
                        }
                    ),
                ],
            }
        )
        return res
