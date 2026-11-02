# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_property_sold(self):
        self.ensure_one()
        self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.buyer_id.id,
            "invoice_line_ids": [
                fields.Command.create({
                    "name": f"{self.name} sale commission",
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06,
                }),
                fields.Command.create({
                    "name": "Administrative fees",
                    "quantity": 1,
                    "price_unit": 100.0,
                }),
            ],
        })
        return super().action_property_sold()
