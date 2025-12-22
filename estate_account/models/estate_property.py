# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for property in self:
            self.env['account.move'].create(
                {
                    'partner_id': property.buyer_id.id,
                    'move_type': 'out_invoice',
                    'invoice_line_ids': [
                        (
                            0,
                            0,
                            {
                                'name': 'Property price',
                                'quantity': 1,
                                'price_unit': property.selling_price,
                            },
                        ),
                        (
                            0,
                            0,
                            {
                                'name': 'Commission (6% of selling price)',
                                'quantity': 1,
                                'price_unit': property.selling_price * 0.06,
                            },
                        ),
                        (
                            0,
                            0,
                            {
                                'name': 'Administrative fees',
                                'quantity': 1,
                                'price_unit': 100.00,
                            },
                        ),
                    ],
                }
            )
        return super().action_sold()
