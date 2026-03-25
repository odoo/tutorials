from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = ['estate.property']  

    def estate_property_action_sold(self):
        self.env['account.move'].create({
            'name': self.name,
            'move_type': 'out_invoice',
            'partner_id': self.buyer_id.id,
            "line_ids": [
                Command.create({
                    "name": "6% of selling price",
                    "quantity": "1",
                    "price_unit": self.selling_price * 0.06,
                }),
                Command.create({
                    "name": "Administrative fee",
                    "quantity": "1",
                    "price_unit": 100.00,
                }),
            ],
        })
        return super().estate_property_action_sold()
