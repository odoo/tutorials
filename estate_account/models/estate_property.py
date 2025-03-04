from odoo import models, fields, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    state = fields.Selection(selection_add=[('invoiced', 'Invoiced')], ondelete={'invoiced': 'cascade'})

    def button_invoice_action(self):
        self.check_access("write")
        invoice_vals = {
            "partner_id": self.buyer_id.id,  
            "move_type": "out_invoice", 
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

        invoice = self.env["account.move"].sudo().create(invoice_vals)
        self.state = 'invoiced'
        print(f"Invoice {invoice.id} created with lines for property {self.id}")  
