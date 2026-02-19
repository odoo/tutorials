from odoo import models, Command

class EstateAccountProperty(models.Model):
    _inherit = "estate_property"

    def property_set_sold(self):
        for record in self:
            self.env['account.move'].create({
                "name": record.name,
                "partner_id": record.buyer_id.id,
                "move_type": "out_invoice",
                "line_ids": [
                    Command.create({
                        "name": "Deposit (6%)",
                        "quantity": 1,
                        "price_unit": record.selling_price*0.06
                    }),
                    Command.create({
                        "name": "Admin fees",
                        "quantity": 1,
                        "price_unit": 100
                    })
                ],
            })
        return super().property_set_sold()