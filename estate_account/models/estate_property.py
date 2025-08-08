from odoo import models,Command

class EstateProperty(models.Model):
    _description = "Estate Account property Model"
    _inherit="estate.property"

    def action_property_sold(self):
         self.check_access("write")
         self.env['account.move'].sudo().create({
              'partner_id' : self.buyer_id.id,
              'move_type' : 'out_invoice',
              'invoice_line_ids' : [
                    Command.create({
                        
                        "name" : "Charges",
                        "quantity" : 1,
                        "price_unit" : 1.06 * self.selling_price,
                   }),
                    Command.create({
                        
                        "name" : "Additional Charges",
                        "quantity" : 1,
                        "price_unit" : 100
                    })
              ]
           })
         return super().action_property_sold()
