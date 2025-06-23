from odoo import models, Command, _


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_mark_sold(self):
        res = super().action_mark_sold()

        for property in self:
            if not property.buyer_id:
                continue

            journal = self.env["account.journal"].search(
                [("type", "=", "sale")], limit=1
            )
            if not journal:
                raise ValueError("No sales journal found!")

            invoice_vals = {
                "partner_id": property.buyer_id.id,
                "move_type": "out_invoice",
                "journal_id": journal.id,
                "invoice_line_ids": [
                    # 6% Commission Line
                    Command.create(
                        {
                            "name": _("Commission Fees"),
                            "quantity": 1,
                            "price_unit": property.selling_price * 0.06,
                        }
                    ),
                    # Flat Admin Fees
                    Command.create(
                        {
                            "name": _("Administrative Fees"),
                            "quantity": 1,
                            "price_unit": 100.00,
                        }
                    ),
                ],
            }

            self.env["account.move"].create(invoice_vals)

        return res
