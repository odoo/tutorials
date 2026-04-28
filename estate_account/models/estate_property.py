from odoo import models, fields, Command


class EstateProperty(models.Model):

    _inherit = "estate.property"

    def action_sold(self):

        self.env["account.move"].create(
            {
                "partner_id": self.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({
                        "name": f"Sales commission: {self.name}",
                        "quantity": 1.0,
                        "price_unit": self.selling_price * 0.06,
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1.0,
                        "price_unit": 100.00,
                    }),
                ],
            }
        )

        return super().action_sold()
