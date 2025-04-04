from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def set_sold(self):
        res = super().set_sold()

        self.check_access('write')

        invoice = self.env['account.move'].sudo().create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price,
                }),
                Command.create({
                    'name': '6% of the selling price',
                    'quantity': 1,
                    'price_unit': 0.06 * self.selling_price,
                }),
                Command.create({
                    'name': 'Administrative fees',
                    'quantity': 1,
                    'price_unit': 100,
                }),
            ],
        })

        return res
