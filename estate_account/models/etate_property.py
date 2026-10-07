from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_do_sold(self):
        super().action_do_sold()

        move_type = "out_invoice"  # Customer Invoice
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        # journal = next(iter(journals))
        for record in self:
            self.env["account.move"].create(
                {
                    "journal_id": journal.id,
                    "move_type": move_type,
                    "partner_id": record.buyer_id.id,
                    "ref": record.name,
                    "invoice_line_ids": [
                        Command.create({
                            "price_unit": record.selling_price * 0.06,
                            "quantity": "1",
                            "name": "Property purchase 6% down payment"
                        }),
                        Command.create({
                            "price_unit": 100.00,
                            "quantity": "1",
                            "name": "Administrative fee"
                        }),
                    ]
                }
            )
