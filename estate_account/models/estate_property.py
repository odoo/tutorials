from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        result = super().action_sold()

        for record in self:
            record.env["account.move"].create(
                {
                    "move_type": "out_invoice",
                    "partner_id": record.buyer_id.id,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "Commission (6%)",
                                "quantity": 1,
                                "price_unit": record.selling_price * 0.06,
                            }
                        ),
                        Command.create(
                            {
                                "name": "Administrative Fees",
                                "quantity": 1,
                                "price_unit": 100,
                            }
                        ),
                    ],
                }
            )

        return result
