from odoo import Command, fields, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    invoice_id  = fields.Many2one('account.move', string="Invoice", readonly=True)

    def property_sold_action(self):
            self.check_access('write')
            self.env['account.move'].sudo().create({
                'partner_id' : self.partner_id.id,
                'move_type' : 'out_invoice',
                'invoice_line_ids': [
                    (0, 0, {
                        'name': self.name,
                        'quantity': 1,
                        'price_unit': self.selling_price * 0.06,
                    }),
                    (0, 0, {
                        'name': 'administrative fees',
                        'quantity': 1,
                        'price_unit': 100,
                    }),
                ],
            })
            return super().property_sold_action()
