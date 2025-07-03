from odoo import models


class InheritedProperty(models.Model):
    _inherit = "estate.property"

    def set_sold_state(self):
        res = super().set_sold_state()

        for property in self:
            property.check_access("write")

            if not property.buyer or not property.selling_price:
                continue

            commission = property.selling_price * 0.06
            admin_fee = 100.0

            self.env["account.move"].sudo().create(
                {
                    "move_type": "out_invoice",
                    "partner_id": property.buyer.id,
                    "invoice_origin": property.name,
                    "invoice_line_ids": [
                        (
                            0,
                            0,
                            {
                                "name": "6% Commission",
                                "quantity": 1,
                                "price_unit": commission,
                            },
                        ),
                        (
                            0,
                            0,
                            {
                                "name": "Administrative Fees",
                                "quantity": 1,
                                "price_unit": admin_fee,
                            },
                        ),
                    ],
                }
            )

        return res
