from odoo import fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        # Check if the property is canceled
        for record in self:
            if record.status == "canceled":
                msg = "A cancelled property cannot be set as sold."
                raise UserError(msg)
            record.status = "sold"

        # Create invoice
        self.env["account.move"].create(
            {
                "partner_id": self.partner_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": self.name,
                            "quantity": 1,
                            "price_unit": self.selling_price,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "6% commission on selling price",
                            "quantity": 1,
                            "price_unit": self.selling_price * 0.06,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "Administrative fees",
                            "quantity": 1,
                            "price_unit": 100.00,
                        },
                    ),
                ],
            }
        )

        return super(EstateProperty, self).action_set_sold()
