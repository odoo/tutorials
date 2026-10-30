from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_mark_sold(self):
        self.ensure_one()
        self.check_access("write")
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        self.env["account.move"].sudo().create(
            {
                "partner_id": self.buyer_id.id,
                "move_type": "out_invoice",
                "journal_id": journal.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": self.name,
                            "quantity": 1,
                            "price_unit": 0.06 * self.selling_price,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Administrative fees",
                            "quantity": 1,
                            "price_unit": 100,
                        }
                    ),
                ],
            }
        )
        return super().action_mark_sold()
