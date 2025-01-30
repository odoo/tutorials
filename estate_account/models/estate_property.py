from odoo import api, fields, models,Command
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

from datetime import date, timedelta


class EstateProperty(models.Model):
    _inherit = "estate_property"

    def action_sold(self):
        
        invoice_values = {
            'partner_id': self.buyer_id.id,  # Assuming buyer_id is linked to res.partner
            'move_type': 'out_invoice',  # Customer Invoice
            'invoice_line_ids': [
                Command.create({
                    'name': 'Commission Fee',
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,  # 6% of the selling price
                }),
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100.00,  # Fixed administrative fee
                })
            ]
        }
        self.env['account.move'].create(invoice_values)
        
        return super().action_sold()
