from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        invoice_vals = {
            "partner_id": self.buyer_id.id,
            "move_type" : "out_invoice",
            # "journal_id":""
            "line_ids": [
                Command.create({
                    "name": self.name,
                    "quantity": 1,
                    "price_unit": self.selling_price*0.06,
                }),
                Command.create({
                    "name": "Administrative Fees",
                    "quantity": 1,
                    "price_unit": 100,
                }),
            ],
        }

        self.env["account.move"].sudo().create(invoice_vals)
        return super().action_set_sold()
