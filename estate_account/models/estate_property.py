from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        print("I am here")
        self.ensure_one()
        self.env["account.move"].create(
            {
                "partner_id": self.buyer_id,
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
                            "name": "administrative fees",
                            "quantity": 1,
                            "price_unit": 100.00,
                        }
                    ),
                ],
            }
        )
        return super().action_sold()
