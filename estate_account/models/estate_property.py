from odoo import Command, fields, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sold_action(self):
        result = super(EstateProperty, self).sold_action()
        invoice = self.env["account.move"].create(
            {
                "partner_id": self.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": self.name,
                            "quantity": 1,
                            "price_unit": 0.06 * self.selling_price,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Administrative Fees",
                            "quantity": 1,
                            "price_unit": 100.00,
                        }
                    ),
                ],
            },
        )

        return result
