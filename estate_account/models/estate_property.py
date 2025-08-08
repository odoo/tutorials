from odoo import Command, fields, models

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    invoice_id  = fields.Many2one('account.move', string="Invoice", readonly=True)

    def action_sold_property(self):
        self.check_access('write')
        res = super().action_sold_property()
        invoice = self.env['account.move'].sudo().create({
            'partner_id': self.partner_id.id,
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
        self.invoice_id = invoice.id
        return res
