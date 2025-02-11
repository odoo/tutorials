from odoo import Command,models
from odoo.exceptions import UserError

class InheritEstateProperty(models.Model):
    _inherit = "estate.property"


    def action_sold(self):
       
        for property in self:
            if not property.buyer_id:
                raise UserError(
                    "Please define a buyer for the property before marking it as sold."
                )
            if not property.selling_price:
                raise UserError(
                    "Selling price must be set before marking the property as sold."
                )
            journal = self.env["account.journal"].search(
                [("type", "=", "sale")], limit=1
            )
            if not journal:
                raise UserError(
                    "No sales journal found! Please configure a sales journal."
                )
            invoice_vals = {
                "partner_id": property.buyer_id.id,
                "move_type": "out_invoice",
                "journal_id": journal.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "Commission (6% of Selling Price)",
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
            self.env["account.move"].create(invoice_vals)
        return  super().action_sold()