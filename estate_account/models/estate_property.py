from odoo import Command, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def mark_offer_sold(self):
        if not self.partner_id.id:
            raise UserError("Property without buyer cannot be sold.")
        try:
            self.env["estate.property"].check_access("write")
        except:
            raise UserError(
                "You do not have the necessary permissions to sell this property."
            )
        self.sudo().env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.partner_id.id,
                "line_ids": [
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
                            "price_unit": 100.0,
                        }
                    ),
                ],
            }
        )

        return super().mark_offer_sold()
