from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for record in self:
            record.env["account.move"].sudo().create(
                {
                    "partner_id": record.buyer_id.id,
                    "move_type": "out_invoice",
                    "currency_id": record.currency_id.id,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": record.name,
                                "quantity": 1,
                                "price_unit": record.selling_price * 0.06,
                                "currency_id": record.currency_id.id,
                            },
                        ),
                        Command.create(
                            {
                                "name": "Administrative Fees",
                                "quantity": 1,
                                "price_unit": 100,
                                "currency_id": record.currency_id.id,
                            },
                        ),
                    ],
                }
            )

        return super().action_sold()
