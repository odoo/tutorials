from odoo import Command, exceptions, models


class EstateProperty(models.Model):
    _inherit = ["estate.property"]
    _name = "estate.property"

    def action_sold(self):
        if not self.buyer_id:
            raise exceptions.UserError('The house need a buyer to be sold. An accepted offer is needed to validate the buyer')
        super().action_sold()
        self.env["account.move"].create({
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "invoice_line_ids": [
                Command.create({
                    "name": self.name,
                    "quantity": "1",
                    "price_unit": self.selling_price / 100 * 6
                }),
                Command.create({
                    "name": "Administartive fee",
                    "quantity": "1",
                    "price_unit": 100
                })
            ]
        })
