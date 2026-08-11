from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_state_sold(self):
        res = super().action_set_state_sold()
        for prop in self:
            self.env["account.move"].create(
                {
                    "partner_id": prop.buyer.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": f"Commission Fee (6%) for {prop.name}",
                                "quantity": 1.0,
                                "price_unit": prop.selling_price * 0.06,
                            },
                        ),
                        Command.create(
                            {
                                "name": f"Administrative Fees for {prop.name}",
                                "quantity": 1.0,
                                "price_unit": 100.00,
                            },
                        ),
                    ],
                },
            )

        return res
