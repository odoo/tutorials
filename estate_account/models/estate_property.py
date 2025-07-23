from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sell(self):
        for rec in self:
            if rec.state != "sold":
                continue

            self.env["account.move"].create(
                {
                    "partner_id": rec.buyer_id.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": f"INV ${rec.name} 1",
                                "quantity": 1,
                                "price_unit": 0.06 * rec.selling_price + 100.00,
                            },
                        ),
                        Command.create(
                            {
                                "name": f"INV ${rec.name} 2",
                                "quantity": 1,
                                "price_unit": 0.06 * rec.selling_price + 100.00,
                            },
                        ),
                    ],
                }
            )

        return super().sell()
