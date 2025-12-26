from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sell_property(self):
        result = super().sell_property()
        for record in self:
            invoice_val = {
                'state': 'draft',
                'move_type': 'out_invoice',
                'partner_id': int(record.buyer_id),
                'line_ids': [
                    Command.create({
                        "name": "First Payment",
                        "quantity": 1,
                        "price_unit": record.selling_price * 0.06
                    }),
                    Command.create({
                        "name": "Administrative Fees",
                        "quantity": 1,
                        "price_unit": 100.00
                    })
                ]
            }
            self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(invoice_val)
        return result
