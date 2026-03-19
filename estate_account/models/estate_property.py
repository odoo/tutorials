from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def change_state_to_sold(self):
        res = super().change_state_to_sold()
        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'line_ids': [
                Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price
                }),
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100.00
                }),
                Command.create({
                    'name': 'Additional Costs',
                    'quantity': 1,
                    'price_unit': 0.06 * self.selling_price
                }),
            ]})
        return res
