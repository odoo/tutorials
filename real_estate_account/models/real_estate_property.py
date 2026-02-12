from odoo import models, Command


class RealEstate(models.Model):
    _inherit = 'real.estate'

    def action_sold(self):
        res = super().action_sold()
        for property in self:
            self.env['account.move'].create({
                'partner_id': property.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': '6% of selling price',
                        'quantity': 1,
                        'price_unit': property.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'Administrative fees',
                        'quantity': 1,
                        'price_unit': 100.0,
                    }),
                ],
            })
        return res
