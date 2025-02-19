from odoo import models,Command
from odoo import fields
from odoo.exceptions import ValidationError,UserError

class EstateProperty(models.Model):
    _inherit = "estate.property"
    state = fields.Selection(selection_add=[('invoiced', 'Invoiced')])
    
    def action_set_sold(self):
        super().action_set_sold()
        self.state = 'invoiced'
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
