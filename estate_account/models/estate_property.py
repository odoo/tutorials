from odoo import models, Command


class EstateProperty(models.Model):

    _inherit = 'estate.property'

    def action_sell_property(self):

        vals_list = []

        for record in self:
            vals = {
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'line_ids': [
                    Command.create({
                        'name': '6% of selling price',
                        'quantity': 1,
                        'price_unit': 0.06 * record.selling_price
                    }),
                    Command.create({
                        'name': 'Administrative fees',
                        'quantity': 1,
                        'price_unit': 100
                    })
                ]
            }
            vals_list.append(vals)

        self.env['account.move'].create(vals_list)

        return super().action_sell_property()
