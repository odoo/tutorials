from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sell_property(self):
        for record in self:
            record.env['account.move'].create({
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': '6% of the selling price',
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'an additional 100.00 from administrative fees',
                        'quantity': 1,
                        'price_unit': 100
                    })
                ]
            })
        return super().sell_property()
