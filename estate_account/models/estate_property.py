from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate_property"

    def action_mark_property_sold(self):
        super().action_mark_property_sold()
        for record in self:
            record.env["account.move"].create(
                {
                    "partner_id": record.buyer_id.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "6% of selling price",
                                "price_unit": 0.06 * record.selling_price,
                                "quantity": 1,
                            }
                        ),
                        Command.create(
                            {
                                "name": "Administrative fees",
                                "price_unit": 100,
                                "quantity": 1,
                            }
                        ),
                    ],
                }
            )
