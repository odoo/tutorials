from odoo import models, Command


class estateAccount(models.Model):
    _inherit = "estate.building"

    def action_set_sold(self):
        self.env["account.move"].create(
            {
                "partner_id": self.buyer_id.id,
                "move_type": "out_invoice",
                "line_ids": [
                    Command.create(
                        {
                            "name": "Property Sale",
                            "quantity": 1.0,
                            "price_unit": self.value,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Taxes",
                            "quantity": 1.0,
                            "price_unit": self.value * 0.06,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Administrative Fees",
                            "quantity": 1.0,
                            "price_unit": 100.0,
                        }
                    ),
                ],
            }
        )
        return super().action_set_sold()
