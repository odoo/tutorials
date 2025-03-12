from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo import Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        result = super().action_set_sold()
        for property in self:
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
                            "name": "Property",
                            "quantity": 1,
                            "price_unit": property.selling_price,
                        }
                    ),
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
            return result
