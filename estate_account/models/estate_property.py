# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = ['estate.property']
    _name = 'estate.property'

    def action_sold(self):
        self.env['account.move'].create(
            {
                'partner_id': self.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create(
                        {
                            'name': self.env._("6% of the selling price"),
                            'quantity': 1,
                            'price_unit': self.selling_price * 0.06,
                        }
                    ),
                    Command.create(
                        {
                            'name': self.env._("100 fees"),
                            'quantity': 1,
                            'price_unit': 100,
                        }
                    ),
                ],
            }
        )
        return super(EstateProperty, self).action_sold()
