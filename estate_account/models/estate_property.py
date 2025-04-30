from datetime import datetime

from odoo import Command, fields, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    invoice_ids = fields.One2many(
        'account.move', 'property_id', string='Invoices', copy=False
    )

    def action_open_invoices(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Property Invoices',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('property_id', '=', self.id)],
            'context': {'default_property_id': self.id},
        }

    def action_sold(self):
        """Automatically create an invoice for the property sale."""
        self.check_access('write')
        if super().action_sold() is True:
            return (
                self.env['account.move']
                .sudo()
                .create({
                    'partner_id': self.buyer_id.id,
                    'invoice_date': datetime.today(),
                    'property_id': self.id,
                    'move_type': 'out_invoice',
                    'invoice_line_ids': [
                        Command.create({
                            'name': self.name,
                            'quantity': 1,
                            'price_unit': self.selling_price * 0.06,
                        }),
                        Command.create({
                            'name': 'Administrative Fees',
                            'quantity': 1,
                            'price_unit': 100,
                        }),
                    ],
                })
            )

        return False
