from odoo import models, Command


class RealEstateProperty(models.Model):
    _inherit = "estate.property"

    def sold_property(self):
        invoice_vals_list = {
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "invoice_line_ids": [
                Command.create(
                    {
                        "name": "6% of the selling price",
                        "quantity": 1,
                        "price_unit": self.selling_price * 0.06,
                    },
                ),
                Command.create(
                    {
                        "name": "Administrative fees",
                        "quantity": 1,
                        "price_unit": 100,
                    },
                ),
            ],
        }

        return self.env["account.move"].create(invoice_vals_list)
