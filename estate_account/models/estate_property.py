from odoo import Command, models


class inheritUsers(models.Model):
    _inherit = 'estate.property'

    def action_mark_sold(self):
        self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.buyer_id.id,
                "invoice_line_ids": [
                    Command.create({
                        "name": self.name,
                        "quantity": 1,
                        "price_unit": 0.06 * self.selling_price,
                    }),
                    Command.create({
                        "name": "administrative_fees",
                        "quantity": 1,
                        "price_unit": 100,
                    })
                ],
            }
        )
        return super().action_mark_sold()
