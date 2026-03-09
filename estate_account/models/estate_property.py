from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        res = super().action_sold()

        for record in self:
            self.env["account.move"].create(
                {
                    "move_type": "out_invoice",
                    "partner_id": record.buyer_id.id,
                    "invoice_line_ids": [
                        [0, 0, {
                                "name": "6% Commission",
                                "quantity": 1,
                                "price_unit": record.selling_price * 0.06,
                        }],
                        Command.create(
                            {
                                "name": "Administrative Fees",
                                "quantity": 1,
                                "price_unit": 100,
                            }
                        ),
                    ],
                }
            )

        return res
