from odoo import Command, models


class TestModel(models.Model):
    _inherit = 'estate.property'

    def action_sell_property(self):
        for record in self:
            self.env['account.move'].create({
                'name': record.name,
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'line_ids': [
                    Command.create({
                        'name': f'Selling property {record.name}',
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100.0,
                    }),
                ],
            })
        return super().action_sell_property()
