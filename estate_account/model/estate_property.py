from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo import Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        for property in self:
            if property.state == "cancelled":
                raise UserError("You cannot mark a cancelled property as sold.")
            if property.state != "offer_accepted":
                raise UserError(
                    "Property must be in 'Offer Accepted' state before selling."
                )

            journal = self.env["account.journal"].search(
                [("type", "=", "sale")], limit=1
            )
            if not journal:
                raise UserError("No sales journal found!")

            invoice_vals = {
                "partner_id": property.buyer.id,
                "move_type": "out_invoice",
                "journal_id": journal.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "Service Fee (6%)",
                            "quantity": 1,
                            "price_unit": property.selling_price * 0.06,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Administrative Fee",
                            "quantity": 1,
                            "price_unit": 100.00,
                        }
                    ),
                ],
            }

            invoice = self.env["account.move"].create(invoice_vals)
            property.state = "sold"
            return invoice
