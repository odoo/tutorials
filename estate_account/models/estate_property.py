from odoo import models
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit='estate.property'

    def action_sold(self):
        for record in self:
            if not record.buyer_id:
                raise UserError("Buyer must be set.") 
            self.env['account.move'].create({
                'partner_id': record.buyer_id.id,   
                'move_type': 'out_invoice', 
                'property_id': record.id, 
                'invoice_line_ids': [
                    (0, 0, {
                       'name': 'Property Sale Commission (6%)',
                       'quantity': 1,
                       'price_unit': record.selling_price * 0.06,
                    }),
                    (0, 0, {
                       'name': 'Administrative Fees',
                       'quantity': 1,
                       'price_unit': 100.00,
                    }),
                ]
            })  
        return super().action_sold()
