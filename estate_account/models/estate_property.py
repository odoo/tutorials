from odoo import models, Command


class Estate(models.Model):
    _inherit = "estate.property"

    def action_sell_property(self):
        for record in self:
            record.env["account.move"].create(
                {
                    "partner_id": record.buyer.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": record.name,
                                "quantity": 1,
                                "price_unit": record.selling_price,
                            },
                        ),
                        Command.create(
                            {
                                "name": "6 Percent of selling price",
                                "quantity": 1,
                                "price_unit": 6 * (record.selling_price) / 100,
                            }
                        ),
                        Command.create(
                            {
                                "name": "Adminstrative Fees",
                                "quantity": 1,
                                "price_unit": (record.selling_price) + 100,
                            }
                        ),
                    ],
                }
            )
        return super().action_sell_property()
