from odoo import Command, models


class EstateAccount(models.Model):
    _inherit = "estate.property"

    def action_mark_as_sold(self):
        partner_id = self.buyer_id.id

        self.env["account.move"].create({
            "partner_id": partner_id,
            "move_type": "out_invoice",
            'invoice_line_ids': [
                Command.create({
                    "name":self.name,
                    "quantity":1,
                    "price_unit":self.selling_price
                }),
                Command.create({
                    "name":"Administrative Fees",
                    "quantity":1,
                    "price_unit":100
                }),
                Command.create({
                    "name":"Tax",
                    "quantity":1,
                    "price_unit":self.selling_price * 0.06
                })
            ]
        })

        return super().action_mark_as_sold()
