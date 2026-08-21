from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for estate_property in self:
            self.env["account.move"].create(
                {
                    "partner_id": estate_property.buyer_id.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": estate_property.name,
                                "quantity": 1.0,
                                "price_unit": estate_property.selling_price * 0.06,
                            }
                        ),
                        Command.create(
                            {
                                "name": "Administrative fees",
                                "quantity": 1.0,
                                "price_unit": 100.0,
                            }
                        ),
                    ],
                }
            )
        return super().action_sold()
