from odoo import Command, models
from psycopg2.extras import wait_select


class EstatePropertyAccount(models.Model):
    _inherit = "estate.property"

    def action_sell_property(self):
        sold = super().action_sell_property()
        for estate_property in self:
            move = estate_property.env["account.move"].create(
                {
                    "partner_id": estate_property.buyer_id.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "6% of selling price",
                                "quantity": 1,
                                "price_unit": estate_property.selling_price * 0.06,
                            },
                        ),
                        Command.create(
                            {
                                "name": "Administration fees",
                                "quantity": 1,
                                "price_unit": 100,
                            },
                        ),
                    ],
                },
            )
        return sold
