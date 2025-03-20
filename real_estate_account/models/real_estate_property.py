from odoo import Command, fields, models
from odoo.exceptions import AccessError

class RealEstatePropertyAccount(models.Model):
    _inherit = 'real.estate.property'

    # Overriding sold method and generating invoice
    def action_property_sold(self):
        self.check_access('write')
        
        print(" reached ".center(100, '='))

        moves = self.env['account.move'].sudo().create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'journal_id': self.env['account.journal'].sudo().search([('type', '=', 'sale')], limit=1).id,
            'invoice_line_ids': [
                Command.create({
                    'name': self.name,
                    'quantity': 1.0,
                    'price_unit': self.selling_price,
                }),
                Command.create({
                    'name': '6% of selling price',
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
