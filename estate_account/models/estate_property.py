from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sell_property(self):
        res = super().action_sell_property()
        for record in self:
            self.env['account.move'].create({
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': "Commission (6%)",
                        'quantity': 1.0,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': "Administrative Fees",
                        'quantity': 1.0,
                        'price_unit': 100.00,
                    })
                ]
            })
        return res
