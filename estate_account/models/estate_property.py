from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        res = super().action_sold()
        journal = self.env["account.journal"].search([
            *self.env["account.journal"]._check_company_domain(self.env.company),
            ("type", "=", "sale"),
        ], limit=1)
        for record in self:
            self.env["account.move"].create(
                {
                    "partner_id": record.buyer_id.id,
                    "move_type": "out_invoice",
                    "journal_id": journal.id,
                    "invoice_line_ids": [
                        Command.create({
                            "name": f"{record.name} - 6% commission",
                            "quantity": 1,
                            "price_unit": record.selling_price * 0.06,
                        }),
                        Command.create({
                            "name": "Administrative fees",
                            "quantity": 1,
                            "price_unit": 100.00,
                        }),
                    ],
                }
            )
        return res
