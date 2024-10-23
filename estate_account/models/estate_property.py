from odoo import Command, models  


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sold_button(self):
        # print("inherited sold action")

        invoice_price = {
            "name": self.name,
            "quantity": 1,
            "price_unit": 0.06 * self.selling_price
        }

        administrative_fees = {
            "name": "Administrative Fees",
            "quantity": 1,
            "price_unit": 100
        }

        self.env['account.move'].create(
            {
                "name": self.name + " Invoice",
                "partner_id" : self.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create(invoice_price),
                    Command.create(administrative_fees)
                ]
            }
        )
        return super().sold_button()
