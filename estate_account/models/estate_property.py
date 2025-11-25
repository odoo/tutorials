from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def button_sell_property(self):
        invoice_name = "INV/ESTATE/" + self.name
        invoice_name2 = "INV/ESTATE/" + self.name + "/Administrative Fees"
        self.env["account.move"].create(
            {
                "partner_id": self.buyer_id,
                "move_type": "out_invoice",
                "line_ids": [
                    Command.create(
                        {
                            "name": invoice_name,
                            "quantity": 1,
                            "price_unit": 0.06 * self.selling_price,
                        },
                    ),
                    Command.create(
                        {
                            "name": invoice_name2,
                            "quantity": 1,
                            "price_unit": 100.00,
                        },
                    ),
                ],
            }
        )
        return super().button_sell_property()
