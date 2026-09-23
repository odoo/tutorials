from odoo import Command, models


class Estaterecorderty(models.Model):
    _inherit = "estate.property"

    def mark_order_as_sold(self):
        res = super().mark_order_as_sold()

        for record in self:
            self.env["account.move"].create(
                {
                    "partner_id": record.buyer.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create({
                            "name": record.name,
                            "quantity": 1,
                            "price_unit": record.selling_price * 0.06,
                        }),
                        Command.create({
                            "name": "Administrative fees",
                            "quantity": 1,
                            "price_unit": 100.0,
                        }),
                    ],
                }
            )

        return res
