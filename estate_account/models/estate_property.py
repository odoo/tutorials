from odoo import models, fields, Command


class InheritedEstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        self.env['account.move'].create(
            {
                'partner_id': self.buyer_id.id, 
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': self.name,
                        'quantity': 1,
                        'price_unit': self.selling_price
                    }),
                    Command.create({
                        'name': r'extra 6% because i feel like it',
                        'quantity': 1,
                        'price_unit': self.selling_price * 0.06
                    }),
                    Command.create({
                        'name': 'administrative fees',
                        'quantity': 1,
                        'price_unit': 100.00
                    })
                ]
            }
        )
        res = super().action_set_sold()
        return res
