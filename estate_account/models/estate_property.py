from odoo import Command, models
from odoo.exceptions import UserError


class estateproperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for record in self:
            if not record.buyer_id:
                raise UserError("The property must have a buyer before creating an invoice.")
            self.env["account.move"].create(
                {
                    "move_type": "out_invoice",
                    "partner_id": record.buyer_id.id,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": record.name,
                                "quantity": 1,
                                "price_unit": 0.06 * record.selling_price,
                            }
                        ),
                        Command.create(
                            {
                                "name": "administrative_fees",
                                "quantity": 1,
                                "price_unit": 100,
                            }
                        ),
                    ],
                }
            )
        return super().action_sold()
