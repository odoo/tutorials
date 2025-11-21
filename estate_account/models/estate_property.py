# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_property_sold(self):
        invoice_vals_list = []
        for record in self:
            if record.state == 'offer_accepted' and record.buyer_id:
                invoice_vals = {
                    'move_type': 'out_invoice',
                    'partner_id': record.buyer_id.id,
                    'invoice_line_ids': [
                        Command.create({
                            "name": "Commission 6%",
                            "quantity": 1,
                            "price_unit": record.selling_price * 0.06,
                        }),
                        Command.create({
                            "name": "Administrative fees",
                            "quantity": 1,
                            "price_unit": 100.,
                        }),
                    ],
                }
                invoice_vals_list.append(invoice_vals)
        self.env['account.move'].sudo().create(invoice_vals_list)
        return super().action_property_sold()
