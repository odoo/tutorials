from odoo import models, Command


class estateaccount(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for record in self:
            self.env["account.move"].create(
                {
                    "name": "test",
                    "move_type": "out_invoice",
                    "partner_id": record.buyer_id.id,
                    "line_ids": [
                        Command.create(
                            {
                                "name": record.title,
                                "quantity": 1.0,
                                "price_unit": 0.06 * (record.selling_price),
                            }
                        ),
                        Command.create(
                            {
                                "name": "Administrative fees",
                                "quantity": 1.0,
                                "price_unit": 100.0,
                            }
                        ),
                    ],
                }
            )
        return super().action_sold()
