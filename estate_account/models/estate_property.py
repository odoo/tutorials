from odoo import models


class InheritedModel(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):
        res = super().action_sold_property()
        invoice_lines = []
        invoice = self.env['account.move'].create({
            'partner_id': self.buyer.id,
            'move_type': 'out_invoice',
        })

        invoice_lines.extend([
            (0, 0, {
                'name': 'Property Sale (6% of Selling Price)',
                'quantity': 1,
                'price_unit': self.selling_price * 0.06,
            }),
            (0, 0, {
                'name': 'Administrative Fees',
                'quantity': 1,
                'price_unit': 100.00,
            }),
        ])

        invoice.write({
            'invoice_line_ids': invoice_lines,
        })
        return res
