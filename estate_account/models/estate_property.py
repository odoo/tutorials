from odoo import models, fields, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def button_sold_action(self):
        """Override Sold button action to create an invoice with invoice lines."""
        res = super().button_sold_action()  
        
        invoice_vals = {
            "partner_id": self.buyer_id.id,  
            "move_type": "out_invoice",  
            "journal_id": self.env["account.journal"].search(
                [("type", "=", "sale")], limit=1
            ).id,  
            "invoice_line_ids": [
                Command.create({
                    "name": self.name,
                    "quantity": 1,
                    "price_unit": self.selling_price,
                }),
                
                Command.create({
                    "name": "Commission Fee",
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06,
                }),
                
                Command.create({
                    "name": "Administrative Fees",
                    "quantity": 1,
                    "price_unit": 100.00,
                }),
            ],
        }

        invoice = self.env["account.move"].create(invoice_vals)

        print(f"Invoice {invoice.id} created with lines for property {self.id}")  # Debugging
        return res  # Return the result of the super() call
