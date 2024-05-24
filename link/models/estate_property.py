from odoo import fields, models, Command


class ResUser(models.Model):
    _inherit = "estate_property"


    def sell_(self):
        print("override")
        account_move = self.env['account.move'].with_context().create({

            'partner_id': self.buyer_id.id,

            'move_type': 'out_invoice',

            'invoice_line_ids': [
                Command.create({
                    'name': '6% of the selling price',
                    'quantity': 1,
                    'price_unit': self.selling_price*0.06,
                }),
                Command.create({
                    'name': 'Administrative fees',
                    'quantity': 1,
                    'price_unit': 100,
                }),
            ],

        })

        return super().sell_()
