from odoo import Command, models


class EstateProperty(models.Model):
    # _name = "estate.account"
    _inherit = "estate.property"

    def sell_apartment(self):
        self.env['account.move'].create({
            'partner_id': self.partner_id.id,
            'move_type': 'out_invoice',
            'line_ids': [
                Command.create({
                    'name': f"Property Sale: {self.name}",
                    'quantity': 1.0,
                    'price_unit': 0.06 * self.selling_price,
                }),
                Command.create({
                    'name': "Administrative Fees",
                    'quantity': 1.0,
                    'price_unit': 100,
                }),
            ],
        })
        return super().sell_apartment()
