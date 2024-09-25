from odoo import Command, models


class estateaccount(models.Model):
    _inherit = "estate.property"

    def sold_button(self):
        for record in self:
            self.env["account.move"].create(
                {
                    "name": "test",
                    "move_type": "out_invoice",
                    "partner_id": record.Buyer_id.id,
                    "line_ids": [
                        Command.create(
                            {
                                "name": record.name,
                                "quantity": 1.0,
                                "price_unit": 0.06 * (record.selling_price),
                            }
                        ),
                        Command.create(
                            {
                                "name": "administrative fee",
                                "quantity": 1.0,
                                "price_unit": 100.0,
                            }
                        ),
                    ],
                }
            )
        return super().sold_button()
