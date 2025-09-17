from odoo import Command, fields, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_set_sold(self):
        super().action_set_sold()

        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price
                }),
                Command.create({
                    'name': self.env._("Administrative Fees"),
                    'quantity': 1,
                    'price_unit': 100
                }),
                Command.create({
                    'name': self.env._("Tax"),
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06
                })
            ]
        })
        return True
