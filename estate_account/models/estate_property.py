from odoo import fields, models, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"
    
    def action_sold_property(self):
        self.env['account.move'].create(
            {
                'partner_id': self.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': self.name,
                        'quantity': 1,
                        'price_unit': self.selling_price,
                    }),

                    Command.create({
                        'name': 'Selling Commision is 6%',
                        'quantity': 1,
                        'price_unit': self.selling_price*0.06,
                    }),

                    Command.create({
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100,
                    })
                ]
            }
        )
        return super().action_sold_property()
    