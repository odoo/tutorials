from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        partner_id = self.buyer_id
        invoice_vals = {'partner_id': partner_id.id,
                        'move_type': 'out_invoice',
                        'invoice_line_ids': [
                            Command.create({
                                'name': self.name,
                                'quantity': 1,
                                'price_unit': self.selling_price * 6 / 100
                                }),
                            Command.create({
                                'name': "Administrative fees",
                                'quantity': 1,
                                'price_unit': 100
                                })
                            ]}

        self.env['account.move'].sudo().with_context(
                default_move_type='out_invoice').create(invoice_vals)

        return super().action_sold()
