from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for estate_property in self:
            move = self.env["account.move"].create(
                {
                    "partner_id": estate_property.salesman_id.id,
                    "move_type": "out_invoice",
                    "line_ids": [
                        Command.create({
                            "name": f"6% of property price",
                            "quantity": 1,
                            "price_unit": 0.06 * estate_property.selling_price
                        }),
                        Command.create({
                            "name": "Administrative fees",
                            "quantity": 1,
                            "price_unit": 100.00
                        })
                    ]
                })

        return super().action_sold()