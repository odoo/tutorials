from odoo import models, Command  # type: ignore


class EstateProperty(models.Model):
    _inherit = "estate_property"

    def action_sold(self):
        fee_amount = 100.00
        commission_amount = 0.06
        values = {
            "partner_id": super().buyer_id.id,
            "move_type": "out_invoice",
            "invoice_line_ids": [
                Command.create(
                    {
                        "name": super().name,
                        "quantity": 1,
                        "price_unit": super().selling_price * commission_amount,
                    }
                ),
                Command.create(
                    {
                        "name": "Administrative fees",
                        "quantity": 1,
                        "price_unit": fee_amount,
                    }
                ),
            ],
        }
        self.env["account.move"].create(values)
        return super().action_sold()
