from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_property_sold(self):
        invoice_price = {
            "name": self.name,
            "quantity": "1",
            "price_unit": self.selling_price * 0.06,
        }
        administrative_fees = {
            "name": "administrative fees",
            "quantity": "1",
            "price_unit": "100",
        }
        self.env["account.move"].create(
            {
                "name": self.name + " invoice",
                "partner_id": self.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create(invoice_price),
                    Command.create(administrative_fees)
                ]
            }
        )
        return self.action_property_cancel()
