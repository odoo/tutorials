from odoo import models
from odoo.exceptions import UserError


class Estate(models.Model):
    _inherit = "estate.estate"

    def action_sell_property(self):
        res = super().action_sell_property()

        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        if not journal:
            raise UserError(
                self.env._(
                    "Please configure an accounting sales journal before selling a property.",
                ),
            )

        for property in self:
            if (
                property.state != "sold"
                or not property.buyer_id
                or not property.selling_price
            ):
                raise UserError(
                    self.env._(
                        "To sell a property, it must be in 'sold' state, have a buyer and a selling price.",
                    ),
                )

            commission_line = (
                0,
                0,
                {
                    "name": f"Commission (6%) for {property.name}",
                    "quantity": 1,
                    "price_unit": property.selling_price * 0.06,
                },
            )

            admin_fee_line = (
                0,
                0,
                {
                    "name": "Administrative Fees",
                    "quantity": 1,
                    "price_unit": 100.00,
                },
            )

            invoice_vals = {
                "partner_id": property.buyer_id.id,
                "move_type": "out_invoice",
                "journal_id": journal.id,
                "invoice_line_ids": [commission_line, admin_fee_line],
            }
            self.env["account.move"].create(invoice_vals)

        return res
