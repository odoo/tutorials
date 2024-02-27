from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def estate_sold(self):
        self.env["account.move"].create({
            "name": "Test",
            "move_type": "out_invoice",
            "partner_id": self.env["estate.property"].buyer_id,
            "invoice_line_ids": [
                Command.create({
                    "name": "Taxe",
                    "quantity": 1,
                    "price_unit": float(self.selling_price) * 0.06
                }),
                Command.create({
                    "name": "Administrative fees",
                    "quantity": 1,
                    "price_unit": 100,
                }),
                Command.create({
                    "name": "Total count",
                    "quantity": 1,
                    "price_unit": float(self.selling_price) * 1.06 + 100.0,
                })
            ]
        })
        return super().estate_sold()
