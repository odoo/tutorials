from odoo import fields, models, exceptions, Command

class EstateAccount(models.Model):
    _inherit = "estate.property"

    def sell_property(self):
        line_ids = [
            Command.create({
                "name": "Price Percentage",
                "quantity": 1,
                "price_unit": self.selling_price * 6 /100,
            }),
            Command.create({
                "name": "Administrative Fees",
                "quantity": 1,
                "price_unit": 100.00,
            })
        ]
        if  not self.buyer_id:
            raise exceptions.UserError("Can't sell a property without a buyer.")
        dictionary = {
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "invoice_line_ids": line_ids
        }
        self.env["account.move"].create(dictionary)

        return super().sell_property()