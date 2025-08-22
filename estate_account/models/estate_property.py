from odoo import Command, models
from odoo.exceptions import UserError, AccessError


class estateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold_property(self):
        self.check_access("write")  # write access for sold action

        result = super().action_set_sold_property()

        try:
            self.env["account.move"].check_access("create")
        except AccessError:
            raise UserError(
                "You do not have the required permissions to create invoices."
            )

        self.env["account.move"].sudo().create(
            {
                "partner_id": self.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "Property Sale Commision",
                            "quantity": 1,
                            "price_unit": self.selling_price * 0.06,
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
            }
        )

        return result
