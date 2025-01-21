from odoo import fields, models, Command

# inheriting the res.user and extending the functionality 
class InheritedEstateProperty(models.Model):
    _inherit= "estate.property"
    
    #overring the sold method
    def action_mark_property_sold(self):
        
        # checking that current user can do update operation on estate.property model or not if not then error on client
        self.env['estate.property'].check_access('write')
        print("action_mark_property_sold in estate account")
        
        # creating a new invoice
        self.env['account.move'].sudo().create({ # used sudo to bypass security for normal agents
            'partner_id': self.buyer.id, #person id who is buying
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    'name': "6% of the selling price",
                    'quantity': 1,
                    'price_unit':self.selling_price*(6/100)
                }),
                Command.create({
                    'name': "an additional 100.00 from administrative fees",
                    'quantity': 1,
                    'price_unit': self.selling_price+100,
                })
            ]
        })
        
        return super().action_mark_property_sold()
