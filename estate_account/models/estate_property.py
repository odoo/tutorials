from odoo import models

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        print("Action sold method overridden!")
        # return super(EstateProperty, self).action_sold()
        res = super(EstateProperty, self).action_sold()
        
        move_vals = {
            'partner_id': self.partner_id.id,
            'move_type': 'out_invoice',
            'invoice_date': self.sold_date,
        }
        move = self.env['account.move'].create(move_vals)
        
        line1_vals = {
            'name': 'Commission (6% of selling price)',
            'quantity': 1,
            'price_unit': self.selling_price * 0.06,
            'move_id': move.id,
        }
        self.env['account.move.line'].create(line1_vals)
        
        line2_vals = {
            'name': 'Administrative fees',
            'quantity': 1,
            'price_unit': 100.00,
            'move_id': move.id,
        }
        self.env['account.move.line'].create(line2_vals)
        
        return res