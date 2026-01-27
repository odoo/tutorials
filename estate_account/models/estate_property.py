from odoo import models, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sell_property(self):
        partner_id = self.buyer.id
        move_type = "out_invoice"
        self.env["account.move"].create({
            "partner_id": partner_id,
            "move_type": move_type,
            "invoice_line_ids": [
                Command.create({
                    "name": "Property price",
                    "price_unit": 0.06 * self.selling_price,
                    "quantity": 1,
                }),
                Command.create({
                    "name": "Administrative fees",
                    "price_unit": 100.0,
                    "quantity": 1,
                })
            ]
        })
        return super().sell_property()    
