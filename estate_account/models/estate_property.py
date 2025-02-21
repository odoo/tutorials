from odoo import models
from odoo import Command

class InheritedModel(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        
        sold_invoice_line = {
            'name': self.name,
            'quantity': 1,
            'price_unit': round(0.06 * self.selling_price, 2),
        }
        
        fees_invoice_line = {
            'name': "Agency Fees",
            'quantity': 1,
            'price_unit': 100,
        }
        
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.buyer.id,
            'invoice_line_ids': [
                Command.create(sold_invoice_line),
                Command.create(fees_invoice_line),
            ],
        }

        # Create customer invoice
        self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(invoice_vals)
        
        return super().action_sold()

