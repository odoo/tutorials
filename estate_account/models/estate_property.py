from odoo import api, models, Command
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        res = super().action_set_sold()
        if not self.buyer_id:
            raise UserError("A buyer must be set before marking as sold.")

        try:
            self.check_access("write")

            print("Access check passed".center(100, "="))
        except Exception as e:
            print(f"Access error: {str(e)}".center(100, "="))
            raise

        invoice_vals = {
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            #"journal_id": self.env["account.journal"].search([("type", "=", "sale")], limit=1).id,
            "invoice_line_ids": [
                Command.create(
                    {
                        "name": "Property Sale: " + self.name,
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
        invoice = self.env["account.move"].sudo().create(invoice_vals)

        return invoice
