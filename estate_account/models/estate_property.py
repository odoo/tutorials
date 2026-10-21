from odoo import Command, models  # ty: ignore[unresolved-import]


class EstateProperty(models.Model):
    _inherit = "estate.property"
    _description = "test module for combining the estate module with account invoicing"

    def sold_property(self):
        journal = self.env["account.journal"].search(
            [
                ("type", "=", "sale"),
            ],
            limit=1,
        )
        moves = (
            self.env["account.move"]
            .with_context(default_move_type="out_invoice")
            .create(
                [
                    {
                        "partner_id": record.buyer.id,
                        "move_type": "out_invoice",
                        "journal_id": journal.id,
                        "invoice_line_ids": [
                            Command.create(
                                {
                                    "name": "6% Commission",
                                    "quantity": 1,
                                    "price_unit": record.selling_price * 0.06,
                                }
                            ),
                            Command.create(
                                {
                                    "name": "Admin Fees",
                                    "quantity": 1,
                                    "price_unit": 100.0,
                                }
                            ),
                        ],
                    }
                    for record in self
                ]
            )
        )

        super().sold_property()
        return moves
