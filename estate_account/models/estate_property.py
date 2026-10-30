from odoo import models


class EstatePropertyAccount(models.Model):
    _inherit = "estate.property"

    def action_property_sold(self):
        result = super().action_property_sold()

        for property in self:
            self.env["account.move"].create(
                {
                    "partner_id": property.buyer.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        (
                            0,
                            0,
                            {
                                "name": "Property Sales Commission",
                                "quantity": 1,
                                "price_unit": property.selling_price * 0.06,
                            },
                        ),
                        (
                            0,
                            0,
                            {
                                "name": "Administrative Fees",
                                "quantity": 1,
                                "price_unit": 100.00,
                            },
                        ),
                    ],
                }
            )
        return result
