from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.buyer_id.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "6% of selling price",
                            "quantity": 1,
                            "price_unit": self.selling_price * 0.6,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Administrative fees",
                            "quantity": 1,
                            "price_unit": 100.0,
                        }
                    ),
                ],
            }
        )
        return super().action_set_sold()
