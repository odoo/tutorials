from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        invoice = {
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "invoice_line_ids": [
                Command.create(
                    {
                        "name": "6% of property price",
                        "quantity": 1,
                        "price_unit": self.selling_price * 0.06,
                    }
                ),
                Command.create({"name": "Charge", "quantity": 1, "price_unit": 100_00}),
            ],
        }
        self.env["account.move"].create(invoice)
        return super().action_sold()
