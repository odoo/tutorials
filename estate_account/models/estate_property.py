
from odoo import fields, models, Command

class EstateProperty(models.Model):
    _inherit = 'estate_property'
    _description = 'Estate Property'

    invoice_id = fields.Many2one('account.move', copy=False, readonly=True)

    def action_sold_estate_property(self):
        self.check_access('write')
        invoice = self.env['account.move'].sudo().create({
            'move_type': 'out_invoice',
            'partner_id': self.buyer_id.id,
            'invoice_line_ids': [Command.create({
                'name': self.name,
                'quantity': 1,
                'price_unit': self.selling_price,
            }),
            Command.create({
                'name': "Commission",
                'quantity': 1,
                'price_unit': self.selling_price * 0.06,
            }),
            Command.create({
                'name': "Administrative Fees",
                'quantity': 1,
                'price_unit': 100.0,
            }),
            ],
        })
        self.invoice_id = invoice

        return super().action_sold_estate_property()
