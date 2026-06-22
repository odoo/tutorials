from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sell_property(self):
        res = super().sell_property()
        for property in self:
            self.env["account.move"].create(
                {
                    "partner_id": property.buyer_id.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "Commission",
                                "price_unit": property.selling_price or property.expected_price,
                                "quantity": 0.06,
                            },
                        ),
                        Command.create(
                            {
                                "name": "Admin fee",
                                "price_unit": 100,
                                "quantity": 1,
                            },
                        ),
                    ],
                },
            )
        return res
