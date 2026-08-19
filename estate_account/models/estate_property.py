from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def set_state_sold(self):
        result = super().set_state_sold()

        for record in self:
            invoice = self.env["account.move"].create(
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
            invoice.action_post()

        return result
