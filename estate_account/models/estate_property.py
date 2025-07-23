from odoo import fields, models, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"
    
    def action_sold(self):
        res = super().action_sold()
        journal = self.env["account.journal"].search([("type", "=","sale")], limit = 1)
        invoice_vals = {
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "journal_id": journal.id,
            "invoice_date": fields.Date.today(), 
            "invoice_line_ids": [
                Command.create({
                    "name": self.name,
                    "quantity": 1,
                    "price_unit": self.selling_price * 6.0 / 100.0
                }),
                Command.create({
                    "name": "Administrative Fees",
                    "quantity": 1,
                    "price_unit": 100.0
                })
            ]
        }
        
        
        invoice = self.env["account.move"].create(invoice_vals)
        
        return res