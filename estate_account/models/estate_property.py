from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):
        self.env["account.move"].create(
            {
                "partner_id": self.customer.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": self.name,
                            "quantity": 1,
                            "price_unit": self.selling_price * 0.6,
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
        return super().action_sold_property()
