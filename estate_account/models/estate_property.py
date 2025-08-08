from odoo import Command, models
from odoo.exceptions import AccessError, UserError


class EstateProperty(models.Model):
    _inherit = ['estate.property']

    # Overrides the action_sold method to generate an invoice when a property is sold.
    def action_sold(self):
        self.ensure_one()
        # Call the parent class method to retain existing behavior
        result = super().action_sold()
        for property in self:
            if not property.buyer_id:
                raise UserError("Property does not have a customer.")

            # Explicit Security Check: Ensure the user has the right to modify this property
            property.check_access("write")
            # Ensure only authorized users can create invoices
            if not (
                self.env.user.has_group("estate.estate_group_user")
                or self.env.user.has_group("estate.estate_group_manager")
            ):
                raise AccessError(
                    "You do not have permission to create an invoice for this property."
                )

            self.env["account.move"].sudo().create(
                {
                    "partner_id": property.buyer_id.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": property.name,
                                "quantity": 1.0,
                                "price_unit": property.selling_price * 0.06,
                            }
                        ),
                        Command.create(
                            {
                                "name": "Administrative Fees",
                                "quantity": 1.0,
                                "price_unit": 100.00,
                            }
                        ),
                    ],
                }
            )
        return result
