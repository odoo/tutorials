from odoo import Command, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        self.check_access("write")

        super().action_sold()

        for prop in self:
            journal = self.env["account.journal"].search(
                [("type", "=", "sale")],
                limit=1,
            )

            if not journal:
                raise UserError("No sales journal found for invoice creation!")

            invoice_lines = [
                Command.create(
                    {
                        "name": prop.name,
                        "quantity": 1.0,
                        "price_unit": prop.selling_price * 0.06,
                        "account_id": journal.default_account_id.id,
                    },
                ),
                Command.create(
                    {
                        "name": "Administrative fees",
                        "quantity": 1.0,
                        "price_unit": 100.0,
                        "account_id": journal.default_account_id.id,
                    },
                ),
            ]

            self.env["account.move"].create(
                {
                    "partner_id": prop.buyer_id.id,
                    "move_type": "out_invoice",
                    "journal_id": journal.id,
                    "invoice_date": fields.Date.context_today(self),
                    "invoice_line_ids": invoice_lines,
                },
            )

        return True
