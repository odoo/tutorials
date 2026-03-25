from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):
        res = super().action_sold_property()

        for property in self:
            if not property.buyer_id:
                continue
            commission = property.selling_price * 0.06
            self.env["account.move"].create(
                {
                    "partner_id": property.buyer_id.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "Commission (6%)",
                                "quantity": 1,
                                "price_unit": commission,
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
                }
            )

        return res
