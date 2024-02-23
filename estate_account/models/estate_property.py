from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def estate_sold(self):
        self.env["account.move"].create({
            "name": "Test",
            "move_type": "out_invoice",
            "partner_id": self.env["estate.property"].buyer_id,
            "line_ids": [
                Command.create({
                    "name": "Taxe",
                    "quantity": "1",
                    "price_unit": str(float(self.selling_price) * 0.06)
                }),
                Command.create({
                    "name": "Administrative fees",
                    "quantity": "1",
                    "price_unit": "100"
                })
            ]
        })
        return super().estate_sold()
