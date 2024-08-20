from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def estate_property_button_sold(self):

        res = super().estate_property_button_sold()

        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    "name": "Property",
                    "quantity": 1,
                    "price_unit": self.selling_price * 1.06
                }),
                Command.create({
                    "name": "Administrative Fees",
                    "quantity": 1,
                    "price_unit": 100.00
                })
            ]
        })

        return res
