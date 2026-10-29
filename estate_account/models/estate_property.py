from odoo import Command, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _inherit = ["estate.property"]

    def action_sold(self):
        for property in self:
            self.env["account.move"].create({
                "partner_id": property.buyer.id,
                "move_type": "out_invoice",
                "line_ids": [
                    Command.create({
                        "name": "Commission",
                        "quantity": 1.0,
                        "price_unit": property.selling_price * 0.06
                    }),
                    Command.create({
                        "name": "Additional administrative fees",
                        "quantity": 1.0,
                        "price_unit": 100.0
                    })
                ]
            })
        return super().action_sold()
