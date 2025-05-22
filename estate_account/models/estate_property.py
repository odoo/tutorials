from odoo import models, Command


class Property(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for property in self:
            self.env["account.move"].create(
                {
                    "partner_id": property.buyer_id.id,
                    "move_type": "out_invoice",
                    "line_ids": [
                        Command.create(
                            {
                                "name": "6% of price",
                                "quantity": 1,
                                "price_unit": 0.06 * property.selling_price,
                            }
                        ),
                        Command.create({"name": "administrative fees", "quantity": 1, "price_unit": 100.00}),
                    ],
                }
            )
        return super().action_sold()
