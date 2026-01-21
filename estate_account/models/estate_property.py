from odoo import fields, models, exceptions, Command

class EstateProperty(models.Model):
    _inherit = ["estate.property"]

    def sell_property(self):
        for r in self :
            vals = {
                'partner_id': r.buyer_id.id, 
                'move_type': 'out_invoice', 
                'journal_id': 1,
                'invoice_line_ids': [
                    Command.create({
                        'name': '6 percent of selling price',
                        'quantity': 1,
                        'price_unit': (r.selling_price * 6 / 100)
                    }),
                    Command.create({
                        'name': 'Administrative fees',
                        'quantity': 1,
                        'price_unit': 100
                    })
                ]
            }
            move = self.env['account.move'].create(vals)
        return super().sell_property()
