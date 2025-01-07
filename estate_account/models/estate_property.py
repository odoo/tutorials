from odoo import models,fields, Command
from datetime import datetime


class EstateInvoice(models.Model):
    _inherit = 'estate.property'

    def sell_action(self):

        print("Inherited model for invocing is working fine")
        
        self.env['account.move'].create(
           {    
             'partner_id': self.partner_id.id,
             'move_type': 'out_invoice',
            #'invoice_date': fields.Date(default= datetime.today()),
             'invoice_line_ids': [
                Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price*0.06 
                                  }),

                Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price+100.00   
                               })
            ]

             
           }
         
        ).action_post()




        return super().sell_action()