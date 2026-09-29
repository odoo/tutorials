from odoo import models, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sell_property(self):
        super().sell_property()     
        for record in self:

            values = {
            "partner_id" : record.buyer_id.id,
            "move_type" : "out_invoice",
            "invoice_line_ids": [
                Command.create({
                    "name": record.name,
                    "quantity": 1.0,
                    "price_unit": record.selling_price * 0.06,
                }),
                Command.create({
                    "name": "Administrative Fees",
                    "quantity": 1.0,
                    "price_unit": 100,
                })
            ],
            }
            self.env["account.move"].create(values)
