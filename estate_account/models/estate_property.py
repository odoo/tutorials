from odoo import models, fields, Command
from datetime import datetime

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_mark_sold(self):
        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    "name": self.name,
                    "quantity": 1,
                    "price_unit": self.selling_price
                }),
                Command.create({
                    "name": "Additional Charges",
                    "quantity": 1,
                    "price_unit": 0.06 * self.selling_price
                }),
                Command.create({
                    "name": "Administrative Charges",
                    "quantity": 1,
                    "price_unit": 100.00
                })
            ]
        })
        return super().action_mark_sold()
