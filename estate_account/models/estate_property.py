from odoo import Command, models
from odoo.exceptions import UserError, AccessError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        # Check if the current user can write to this property
        self.check_access("write")

        self.sudo().env["account.move"].create(
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
                            "name": "administrative fees",
                            "quantity": 1,
                            "price_unit": 100,
                        }
                    ),
                ],
            }
        )

        return super(EstateProperty, self).action_sold()
