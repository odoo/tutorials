from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold_btn(self):
        self.check_access("write")
        self.env["account.move"].sudo().create({
            "move_type": "out_invoice",
            "partner_id": self.buyer.id,
            "line_ids":[
                Command.create(
                    {
                    "name": self.name,
                    "quantity": 1,
                    "price_unit": 0.06 * self.selling_price
                    }
                ),
                Command.create(
                    {
                    "name": "Administrative fees",
                    "quantity": 1,
                    "price_unit": 100.00
                    }
                )
            ]
        })
        return super().action_sold_btn()
