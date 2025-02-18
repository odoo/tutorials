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
                'partner_id' : self.property_buyer_id.id,
                'move_type'  : 'out_invoice',
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

