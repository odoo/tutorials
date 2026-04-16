from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        result = super().action_sold()

        for rec in self:
            self.env["account.move"].create({
            "partner_id": rec.buyer_id.id,
            "move_type": "out_invoice",
            "invoice_line_ids": [
                Command.create({
                    "name": rec.name,
                    "quantity": 1,
                    "price_unit": rec.selling_price * 0.06,
                }),
                Command.create({
                    "name": "Administrative Fees",
                    "quantity": 1,
                    "price_unit": 100.00,
                }),
            ],
        })

        return result
