from odoo import models, fields, api,Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
       
        res = super().action_sold()  

        invoice_vals = {
            'partner_id': buyer.id, 
            'move_type': 'out_invoice',
            'line_ids': [
                 Command.create({
                    'name': 'Real Estate Sale Commission',  
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,  
                }),
                 Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100.00, 
                }),
            ],
        }
        invoice = self.env['account.move'].create(invoice_vals)
        return res
