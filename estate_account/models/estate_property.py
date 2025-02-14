from odoo import Command, models
from odoo.exceptions import UserError, AccessError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        if not self.buyer_id.id:
            raise UserError("Property without buyer cannot be sold.")
        # Ensure that the current user has write access to the property
        try:
            # Check if the current user can write to this property
            self.check_access_rights("write")
            self.check_access_rule(
                "write"
            )  # Optional: additional check for record rules
        except AccessError:
            raise UserError("You do not have permission to modify this property.")

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
