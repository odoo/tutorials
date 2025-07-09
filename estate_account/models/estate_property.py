from odoo import models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        res = super().action_sold()

        for property in self:
            if property.buyer_id:
                invoice_vals = {
                    'partner_id': property.buyer_id.id,
                    'move_type': 'out_invoice',
                    'invoice_line_ids': [
                        (0, 0, {
                            'name': '6% of Selling Price',
                            'quantity': 1,
                            'price_unit': property.selling_price * 0.06,
                        }),
                        (0, 0, {
                            'name': 'Administrative Fees',
                            'quantity': 1,
                            'price_unit': 100.00,
                        }),
                    ],
                }
                self.env['account.move'].create(invoice_vals)

        return res
