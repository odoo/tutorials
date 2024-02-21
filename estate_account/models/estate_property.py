from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def property_sold(self):
        for record in self:
            self.env["account.move"].create(
                {
                    "partner_id": record.buyer_id.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": record.name,
                                "price_unit": record.selling_price,
                                "quantity": 1,
                            }
                        ),
                        Command.create(
                            {
                                "name": "6% markup",
                                "price_unit": record.selling_price * 0.06,
                                "quantity": 1,
                            }
                        ),
                        Command.create(
                            {
                                "name": "administration fees",
                                "price_unit": 100,
                                "quantity": 1,
                            }
                        ),
                    ],
                }
            )
        return super().property_sold()
