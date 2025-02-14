from odoo import Command, models

class EstateAccount(models.Model):
    _inherit = "estate.property"

    def action_property_sold(self):

        self.check_access('write')

        self.env["account.move"].sudo().create(
            {
                "move_type": "out_invoice",
                "partner_id": self.buyer_id.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "Property Sale",
                            "quantity": 1,
                            "price_unit": 1.06 * self.selling_price,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Additional Charges",
                            "quantity": 1,
                            "price_unit": self.selling_price + 100,
                        }
                    ),
                ],
            }
        )
        return super().action_property_sold()
