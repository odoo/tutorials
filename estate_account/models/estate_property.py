from odoo import models, Command

class EstatePropertyInherited(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        res = super().action_sold()

        AccountMove = self.env["account.move"]
        sales_journal = self.env["account.journal"].search(
            [("type", "=", "sale")],
            limit=1,
        )

        for property in self:
            if not property.buyer_id or not property.selling_price:
                continue

            invoice_vals = {
                "partner_id": property.buyer_id.id,
                "move_type": "out_invoice",
                "journal_id": sales_journal.id,
                "invoice_line_ids": [
                    Command.create({
                        "name": f"Commission (6%) for {property.name}",
                        "quantity": 1,
                        "price_unit": property.selling_price * 0.06,
                    }),
                    Command.create({
                        "name": f"Selling price for {property.name}",
                        "quantity": 1,
                        "price_unit": property.selling_price,
                    }),
                ],
            }

            invoice = AccountMove.create(invoice_vals)
            invoice.action_post()  # optional: automatically post invoice

        return res
