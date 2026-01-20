from odoo import Command, models
from odoo.tools.float_utils import float_round


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for record in self:
            journal = self.env["account.journal"].search(
                [
                    *self.env["account.journal"]._check_company_domain(
                        self.env.company
                    ),
                    ("type", "=", "sale"),
                ],
                limit=1,
            )
            precision_digits = self.env["decimal.precision"].precision_get("Account")
            invoice_vals = {
                "partner_id": record.buyer_id.id,
                "move_type": "out_invoice",
                "journal_id": journal.id,
                "line_ids": [
                    Command.create({
                        "name": "Down Payment",
                        "quantity": 1,
                        "price_unit": float_round(
                            record.selling_price * 0.06,
                            precision_digits=precision_digits,
                        ),
                    }),
                    Command.create({
                        "name": "Administrative Fees",
                        "quantity": 1,
                        "price_unit": 100.00,
                    }),
                ],
            }

            self.env["account.move"].create(invoice_vals)
        return super().action_sold()
