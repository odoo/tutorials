from odoo import fields,api,models

class EstateProperty(models.Model):
    _inherit='estate.property'

    def action_sold(self):
        
        for record in self:
            if not record.buyer:
                raise ValueError("Buyer must be set before generating an invoice.") 
            journal = self.env['account.journal'].search(
                [('type','=','sale')], limit=1
            )
            if not journal:
                raise ValueError("No Sales Journal found. Please configure one.")
            self.env['account.move'].create({
                'partner_id': record.buyer.id,  
                'move_type': 'out_invoice',  
                'journal_id': journal.id, 
                'invoice_line_ids':[
                    (0,0,{
                        'name': 'Property Sale Commission (6%)',
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    (0,0,{
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                ]
            })  
        return super().action_sold()
