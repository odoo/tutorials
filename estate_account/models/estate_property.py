from odoo import api, Command, fields, models


class EstateProperty(models.Model):
    # _name = "estate.property"
    _inherit = "estate.property"

    def action_sell_property(self):
        self.env['account.move'].create({
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "invoice_line_ids": [
                Command.create({
                    "name": self.name,
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06
                }),
                Command.create({
                    "name": "admin fee",
                    "quantity": 1,
                    "price_unit": 100.00
                })
            ]
        })
        return super().action_sell_property()
