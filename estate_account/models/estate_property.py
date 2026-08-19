from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_state_sold(self):
        result = super().action_state_sold()
        invoices = []

        for record in self:
            invoices.append(
                {
                    "partner_id": record.buyer_id.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "Down Payment",
                                "quantity": 1,
                                "price_unit": record.selling_price * 0.06,
                            }
                        ),
                        Command.create(
                            {
                                "name": "Administrative Fees",
                                "quantity": 1,
                                "price_unit": 100.00,
                            }
                        ),
                    ],
                }
            )

        invoice = self.env["account.move"].create(invoices)
        invoice.action_post()

        return result
