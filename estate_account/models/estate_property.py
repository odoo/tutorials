from odoo import models, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        res = super().action_sold()
        for prop in self:
            self.env['account.move'].create({
                'partner_id' : prop.buyer_id.id,
                'move_type' : 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name' : '6% of selling price',
                        'quantity' : 1,
                        'price_unit' : prop.selling_price * 0.06,
                    }),
                    Command.create({
                        'name' : 'Administrative fees',
                        'quantity' : 1,
                        'price_unit' : 1000,
                    }),
                ]
            })
        print("test run")
        return res
