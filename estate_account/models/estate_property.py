from odoo import models,Command
class EstateProperty(models.Model):
    _inherit="estate.property"
    
    def sold(self):
        res= super().sold()
        for rec in self:
            self.env["account.move"].create(
                {
                    "move_type":"out_invoice",
                    "partner_id":rec.buyer_id,
                    "invoice_line_ids":[
                       Command.create({
                        'name':'Random',
                        'quantity':'1',
                        'price_unit':rec.selling_price*0.06,
                       }),
                        Command.create(
                             {
                                 "name": "Administrative Fees",
                                 "quantity": 1,
                                 "price_unit": 100,
                             }
                         ),
                        
                    ]    
                }
            )
        return res
