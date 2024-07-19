from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        for record in self:
            record.check_access_rights('write')
            record.check_access_rule('write')
            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': self.buyer_id.id,
                'invoice_line_ids': [
                    Command.create({
                        'name': record.name,
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06
                    }),
                    Command.create({
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100
                    })
                ]
            }
            record.env['account.move'].sudo().create(invoice_vals)

        ans = super().action_sold()
        return ans
