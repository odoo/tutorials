from odoo import Command, models


class Property(models.Model):
    _inherit = 'estate.property'

    def action_sell_property(self):
        res = super().action_sell_property()

        for record in self:
            self.env['account.move'].create({
                'partner_id': record.buyer.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': record.name,
                        'quantity': 1,
                        'price_unit': 0.06 * record.selling_price
                    }),
                    Command.create({
                        'name': 'Admin fee',
                        'quantity': 1,
                        'price_unit': 100
                    })
                ]
            })
        return res
