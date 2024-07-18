from odoo import models, Command


class InheritedModel(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.user_id.id,
            'invoice_line_ids': [
                Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06
                    }),
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100
                    })
                ]
            }
        self.env['account.move'].sudo().create(invoice_vals)

        ans = super().action_set_sold()
        return ans
