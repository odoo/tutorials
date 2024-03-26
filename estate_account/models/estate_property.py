from odoo import models, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"


    def action_is_sold(self):
        self.ensure_one()
        self.env["account.move"].create(
            {
                "partner_id": self.buyer_id.id,
                "move_type": "out_invoice",
                "line_ids": [
                    Command.create({
                        "name": f"6% downpayment on property {self.name}",
                        "quantity": 1,
                        "price_unit": self.selling_price * 0.06
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1,
                        "price_unit": 100
                    })
                ]
            }
        )
        return super().action_is_sold()
