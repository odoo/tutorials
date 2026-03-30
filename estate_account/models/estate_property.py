from odoo import models, Command


class EstateProperty(models.Model):
    _name = 'estate.property'
    _inherit = 'estate.property'

    def action_sold(self):
        for estate_property in self:
            self.env['account.move'].create({
                'name': estate_property.name,
                'move_type': 'out_invoice',
                'partner_id': estate_property.buyer_id.id,
                'line_ids': [
                    Command.create({
                        'name': estate_property.env._("6% of selling price"),
                        'quantity': '1',
                        'price_unit': estate_property.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': estate_property.env._("Administrative fee"),
                        'quantity': '1',
                        'price_unit': 100.00,
                    }),
                ],
            })
        return super().action_sold()
