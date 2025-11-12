from odoo import Command,models,fields
from odoo.exceptions import AccessError
class EstateProperty(models.Model):
    _description = "Estate Account property Model"
    _inherit="estate.property"
    invoice_line_ids = fields.One2many('account.move','property_id')
    quantity=fields.Integer(string="Quantity")
    
    def action_set_property_as_sold(self):
        #checking access rights
        try:
            self.check_access('write') 
        except AccessError as e:
            raise AccessError("You do not have permission to update this property.")


        move_values = {
            'partner_id': self.buyer_id.id,  
            'move_type': 'out_invoice',
            'property_id':self.id,
            'invoice_line_ids': [
                Command.create({
                    "name":self.name,
                    "quantity": 1,
                    "price_unit": 0.6 * self.selling_price, # 6% of the S.P
                }),
                
                Command.create({
                    "name": "Administrative fees",
                    "quantity": 1,
                    "price_unit": 100.00,
                }),
            ]
        }
        print(" reached ".center(100, '='))
        self.env['account.move'].sudo().create(move_values)
        
        return super().action_set_property_as_sold()