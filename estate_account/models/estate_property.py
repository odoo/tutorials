from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sell_property(self):
        partner_id = self.buyer_id.id
        move_type = "out_invoice"
        self.env["account.move"].create(
            {
                "partner_id": partner_id,
                "move_type": move_type,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "Selling Price",
                            "quantity": 1,
                            "price_unit": 0.06 * self.selling_price,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Administrative Fees",
                            "quantity": 1,
                            "price_unit": 100,
                        }
                    ),
                ],
            }
        )
        return super().sell_property()
