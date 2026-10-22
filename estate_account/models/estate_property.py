from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        is_sold = super().action_sold()
        if is_sold:
            for record in self:
                self.env["account.move"].create(
                    {
                        "partner_id": record.buyer_id.id,
                        "move_type": "out_invoice",
                        "invoice_line_ids": [
                            Command.create(
                                {
                                    "name": "6% of selling price",
                                    "quantity": 1,
                                    "price_unit": record.selling_price * 0.06,
                                }
                            ),
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
        return is_sold
