from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold_property(self):
        res = super().action_sold_property()
        self.env['account.move'].create(
            {
                'partner_id': self.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': self.env._("6% of the selling price"),
                        'quantity': 1,
                        'price_unit': 0.06 * self.selling_price,
                    }),
                    Command.create({
                        'name': self.env._("administrative fees"),
                        'quantity': 1,
                        'price_unit': 100,
                    })
                ]
            }
        )
        return res
