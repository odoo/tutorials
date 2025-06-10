from odoo import models


class EstateProperty(models.Model):
    _inherit = "estate.property"
    _description = "Estate Property Model with Account Move"

    def action_sold(self):
        for record in self:
            record.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': record.partner_id.id,
                'invoice_line_ids': [
                    (0, 0, {
                        'name': 'Property Price',
                        'quantity': 1,
                        'price_unit': record.selling_price,
                    }),
                    (0, 0, {
                        'name': '6% Commission',
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    (0, 0, {
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                ],
            })
        return super().action_sold()
