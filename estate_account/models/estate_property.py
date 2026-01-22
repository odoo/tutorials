from odoo import models
from odoo.fields import Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        super().action_sold()
        self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.buyer_id.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": self.name,
                            "price_unit": self.selling_price * 0.06,
                            "quantity": 1,
                        },
                    ),
                    Command.create(
                        {
                            "name": "Administrative Fees",
                            "price_unit": 100,
                            "quantity": 1,
                        },
                    ),
                ],
            },
        )
        return True
