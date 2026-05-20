from odoo import Command, models

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        res =  super().action_sold()

        for prop in self:

            self.env["account.move"].create({
                "partner_id": prop.buyer_id.id,
                "move_type": "out_invoice",
                "line_ids": [
                    Command.create({
                        "name" : "Agency COmmission",
                        "quantity" : 1.0,
                        "price_unit" : prop.selling_price * 0.06
                    }),
                    Command.create({
                        "name" : "Administrative Fees",
                        "quantity": 1.0,
                        "price_unit" : 100,
                    })
                ],            
            })
            
        return res