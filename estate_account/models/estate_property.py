from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = ["estate.property"]

    def sell_property(self):
        for prop in self:
            vals = {
                'partner_id': prop.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': '6 percent of selling price',
                        'quantity': 1,
                        'price_unit': (prop.selling_price * 6 / 100)
                    }),
                    Command.create({
                        'name': 'Administrative fees',
                        'quantity': 1,
                        'price_unit': 100
                    })
                ]
            }
            self.env['account.move'].create(vals)
        return super().sell_property()
