from odoo import Command, models
from datetime import date


class Estate_Property(models.Model):
    _inherit = "estate_property"

    def action_sold(self):
        super().action_sold()

        for record in self:
            record.env["account.move"].create(
                {
                    "partner_id": record.buyer.id,
                    "move_type": "out_invoice",
                    "invoice_date": date.today(),
                    "journal_id": (
                        record.env["account.journal"].search(
                            [("type", "=", "sale")], limit=1
                        )
                    ).id,
                    "line_ids": [
                        Command.create(
                            {
                                "name": record.name,
                                "quantity": 1,
                                "price_unit": 0.06 * record.selling_price,
                            }
                        ),
                        Command.create(
                            {
                                "name": "Administrative fee",
                                "quantity": 1,
                                "price_unit": 100,
                            }
                        ),
                    ],
                }
            )

        return True
