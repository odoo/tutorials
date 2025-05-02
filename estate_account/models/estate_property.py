from odoo import models, Command
from odoo.exceptions import UserError, AccessError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        self.check_access("write")

        result = super().action_set_sold()

        invoice_vals = {
            "partner_id": self.buyer.id,
            "move_type": "out_invoice",
            "invoice_line_ids": [
                Command.create(
                    {
                        "name": "Property",
                        "quantity": 1,
                        "price_unit": self.selling_price,
                    }
                ),
                Command.create(
                    {
                        "name": "Service Fee (6%)",
                        "quantity": 1,
                        "price_unit": self.selling_price * 0.06,
                    }
                ),
                Command.create(
                    {"name": "Administrative Fee", "quantity": 1, "price_unit": 100.00}
                ),
            ],
        }

        try:
            self.env["account.move"].check_access("create")
        except AccessError:
            raise UserError(
                "You do not have the required permissions to create invoices."
            )

        self.env["account.move"].sudo().create(invoice_vals)

        return result
