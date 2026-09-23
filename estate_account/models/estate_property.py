from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sell_property_state(self):
        for record in self:
            partner_id = record.buyer_id.id
            pre_payment = record.selling_price * 0.06
#           Create the invoice:
            self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create({
                'name': 'Property Invoice',
                'partner_id': partner_id,
                'line_ids': [
                    Command.create({
                        'name': 'Pre-payment',
                        'quantity': 1,
                        'price_unit': pre_payment,
                    }),
                    Command.create({
                        'name': 'Administrative fees',
                        'quantity': 1,
                        'price_unit': 100000
                    })
                ]
            })
        return super().action_sell_property_state()
