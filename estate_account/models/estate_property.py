from odoo import models,Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,  
            'move_type': 'out_invoice',
            'invoice_line_ids': [
            Command.create({
            'name': self.name,
            'quantity': 1.0,
            'price_unit': self.selling_price 
        }),
            Command.create({
            'name': 'Property Sale Commission (6%)',
            'quantity': 1.0,
            'price_unit': self.selling_price * 0.06,
        }),
        Command.create({
            'name': 'Administrative Fees',
            'quantity': 1.0,
            'price_unit': 100.00,
        })
        ]
        })
        return super().action_set_sold()
        