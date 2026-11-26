from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold_estate(self):
        res = super().action_sold_estate()
        for prop in self:
            self.env['account.move'].create(
                {
                    'partner_id': prop.buyer.id,
                    'move_type': 'out_invoice',
                    'line_ids': [
                        Command.create({
                            'name': prop.name,
                            'quantity': 1,
                            'price_unit': prop.selling_price * 1.06,
                        }),
                        Command.create({
                            'name': 'Administrative Fees',
                            'quantity': 1,
                            'price_unit': 100.00,
                        }),
                    ]
                }
            )
        return res
