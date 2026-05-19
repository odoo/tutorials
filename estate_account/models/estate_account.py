from odoo import Command, models


class EstateAccount(models.Model):
    _inherit = "estate.property"

    def action_sold_button(self):
        for prop in self:
            self.env["account.move"].create(
                {
                    "partner_id": prop.buyer_id.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create({
                            "name": prop.name,
                            "quantity": 1,
                            "price_unit": prop.selling_price * 0.06,
                        }),
                        Command.create({
                            "name": "Administrative fees",
                            "quantity": 1,
                            "price_unit": 100,
                        }),
                    ],
                }
            )
        return super().action_sold_button()
