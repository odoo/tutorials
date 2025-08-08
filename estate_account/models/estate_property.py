from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        invoice_vals = {
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    'name': '6% of selling price',
                    'quantity': 1,
                    'price_unit': 0.06 * self.selling_price
                }),
                Command.create({
                    'name': 'administrative fees',
                    'quantity': 1,
                    'price_unit': 100
                }),
            ]
        }
        user_id = self.env['estate.property'].browse(self.env.uid)
        if user_id.check_access('write'):
            self.env['account.move'].sudo().create(invoice_vals)

        return super().action_sold()
