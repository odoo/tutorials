from odoo import fields, models, Command

class estate_property(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        empty_move = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.buyer_id.id, 
            'date': fields.Date.today(), 
            # 'state': 'cancel',  
            'invoice_line_ids': [
                Command.create({
                    'name': self.name,
                    'quantity': 1,  
                    'price_unit': self.selling_price,  
                    'account_id': self.env['account.account'].search([('deprecated', '=', False)], limit=1).id, 
                }),
                Command.create({
                    'name': '6 percent of Selling Price',
                    'quantity': 1,  
                    'price_unit': self.selling_price * 0.06,  
                    'account_id': self.env['account.account'].search([('deprecated', '=', False)], limit=1).id, 
                }),
                Command.create({
                    'name': 'Administrative Fee',
                    'quantity': 1, 
                    'price_unit': 100.0, 
                    'account_id': self.env['account.account'].search([('deprecated', '=', False)], limit=1).id, 
                }),
            ]
        })

        print("empty_move-------------------------",empty_move)

        # empty_move.action_post()
        return super().action_sold()