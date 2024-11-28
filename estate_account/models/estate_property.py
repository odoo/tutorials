from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        self.env['estate.property'].check_access('write')
        for record in self:
            invoice_vals = {
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create(
                        {
                            'name': record.name,
                            'quantity': 1,
                            'price_unit': record.selling_price * 0.06,
                        }
                    ),
                    Command.create(
                        {
                            'name': "Administrative Fees",
                            'quantity': 1,
                            'price_unit': 100,
                        }
                    ),
                ],
            }
            self.env['account.move'].sudo().create(invoice_vals)

            return super().action_sold()
