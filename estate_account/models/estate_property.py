from odoo import fields,api,models

class EstateProperty(models.Model):
    _inherit='estate.property'

    def action_sold(self):
        res = super(EstateProperty, self).action_sold()

        # self.create_invoice()
        
        return res
    

    # def create_invoice(self):
    #     account_invoice = self.env['account.move'].create({
    #         'move_type': 'out_invoice', 
    #         'partner_id': self.partner_id.id,  
    #         'invoice_date': fields.Date.today(), 
    #         'invoice_line_ids': [(0, 0, {
    #             'name': self.name,  
    #             'quantity': 1,  
    #             'price_unit': self.price,  
    #         })],
    #     })
    #     account_invoice.action_post() 