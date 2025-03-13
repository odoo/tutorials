from odoo import api, models, Command

class property(models.Model):
    _inherit = 'estate.property' 
    
    def set_sold(self):
        # print("Hello child property sold")
        empty_move=self.env['account.move'].create({
            # 'name':self.name,
            'partner_id': self.buyer_user_id.id,
            'move_type':'out_invoice',
            'invoice_line_ids':[
                Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price,
                }),
                Command.create({
                    'name': '6% of the selling price',
                    'quantity': 1,
                    'price_unit': 0.6 * self.selling_price,
                }),
                Command.create({
                    'name': 'Administrative fees',
                    'quantity': 1,
                    'price_unit': 100,
                }),
            ],
        })
        return super().set_sold()