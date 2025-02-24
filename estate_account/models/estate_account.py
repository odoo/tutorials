from odoo import models, Command


class InheritedPropertyAccount(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for estate_property in self:
            move = estate_property.env["account.move"].create(
                {
                    "partner_id": estate_property.buyer_id.id,
                    "move_type": "out_invoice",
                    "line_ids": [
                        Command.create(
                            {
                                "name": "pre-payment",
                                "quantity": "1",
                                "price_unit": estate_property.selling_price * 0.06,
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
        return super().action_sold()
