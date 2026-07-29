from odoo import Command, models


class PropertyAccount(models.Model):
    _inherit = "realestate.properties"

    def action_sold_btn(self):
        for record in self:
            journal = self.env["account.journal"].search(
                [("type", "=", "sale")],
                limit=1,
            )
            self.env["account.move"].create(
                {
                    "partner_id": record.buyer_id.id,
                    "move_type": "out_invoice",
                    "journal_id": journal.id if journal else False,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "6% fee",
                                "quantity": 1,
                                "price_unit": record.selling_price * 0.06,
                            }
                        ),
                        Command.create(
                            {
                                "name": "Administrative fix fees",
                                "quantity": 1,
                                "price_unit": 100.0,
                            },
                        ),
                    ],
                },
            )
        return super().action_sold_btn()
