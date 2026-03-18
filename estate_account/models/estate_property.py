from odoo import fields, models, Command


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'EstateProperty'
    _inherit = 'estate.property'
    
    def button_sold(self):
        selling_price = self.selling_price * 0.06
        self.env['account.move'].create({
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "line_ids": [
                Command.create({
                    "name": "6% of selling price",
                    "quantity": 1,
                    "price_unit": selling_price,
                }),
                Command.create({
                    "name": "Administrative Fees",
                    "quantity": 1,
                    "price_unit": 100.00,
                })
            ],
        })
        print("WORKS!!")
        return super().button_sold()
