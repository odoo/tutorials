from datetime import datetime

from odoo import models,fields,Command

class EstatePropertyAccount(models.Model):
    _inherit='estate.property'

    def sold_event(self):

        #record.status='sold'

        try:
            self.check_access_rights('write')  
            self.check_access_rule('write')

            print("Access check passed".center(100, '='))
        except Exception as e:
            print(f"Access error: {str(e)}".center(100, '='))
            raise

        invoice_vals={
                'name': f"INV/{datetime.today().year}/{self.property_buyer_id.id}{self.id}",
                'partner_id' : self.property_buyer_id.id,
                'move_type'  : 'out_invoice',
                # 'journal_id' : self.env['account.journal'].search([('type', '=', 'sale')], limit=1).id,
                'invoice_date': fields.Date.today(),
                'invoice_line_ids' : [
                    Command.create({
                        'name': self.name,
                        'price_unit': self.selling_price
                    }),
                    Command.create({
                        'name': self.name,
                        'price_unit':self.selling_price*0.06
                    }),
                    Command.create({
                        'name' : self.name,
                        'price_unit':100
                    })
                ]

        }
        invoice = self.env['account.move'].sudo().create(invoice_vals)
        return super().sold_event()

    
    """

    'invoice_line_ids': [(0, 0, { # found in accout_move_line and it is one2many model and foregin key inside account_move is move_id in this table
                    'name': self.name,  # Name of the property , the 0,0 refers to new record like first 0 tells to create new record and second one is ?(search for second one)
                    'quantity': 1,  # Selling one property
                    'price_unit': self.selling_price,  # Selling price of the property
                })] 
"""