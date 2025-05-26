from odoo import models, Command
from odoo.exceptions import AccessError, UserError
from odoo.tools import float_is_zero


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        self._create_invoices()
        return super().action_sold()

    def _create_invoices(self):
        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    'name': f'The property {self.name}',
                    'quantity': 1,
                    'price_unit': self.selling_price,
                }),
                Command.create({
                    'name': f'Tax 6% {self.name}',
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,
                }),
                Command.create({
                    'name': 'Administrative fees',
                    'quantity': 1,
                    'price_unit': 100.0,
                })
            ]
        })
