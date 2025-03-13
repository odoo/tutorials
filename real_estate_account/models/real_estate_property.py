from odoo import fields, models, Command
from datetime import datetime

class RealEstatePropertyAccount(models.Model):
    _inherit = 'real.estate.property'

    # Overriding sold method and generating invoice
    def action_property_sold(self):
        moves = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'invoice_line_ids': [
                Command.create({
                    'name': self.name,
                    'quantity': 1.0,
                    'price_unit': (self.selling_price * 0.06),
                }),
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1.0,
                    'price_unit': 100.00,
                }),
            ]
        })
        return super().action_property_sold()
