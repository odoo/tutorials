from odoo import Command, models

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_property_sold(self):
        for record in self:
            self.env["account.move"].create(
                {
                    "partner_id": record.buyer.id,
                    "move_type": 'out_invoice',
                    "line_ids": [
                        Command.create({
                            "name": "Selling price 6 percent",
                            "price_unit": record.selling_price * 0.06,
                            "quantity": 1,
                        }),
                        Command.create({
                            "name": "Administrative fees",
                            "price_unit": 100,
                            "quantity": 1,
                        })
                    ],
                }
            )
        return super().action_property_sold()