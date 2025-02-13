from odoo import models, fields, Command

class EstateProperty(models.Model):
    
    _inherit = "estate.property"
    
    def action_sold(self):
        res = super().action_sold()
        for property in self:
            self.env['account.move'].create(
            {
                "partner_id" : property.buyer_id.id,
                "move_type" : "out_invoice",
                "invoice_line_ids" : [
                    Command.create({
                        "name": property.name,
                        "quantity": 1.0,
                        "price_unit" : (property.selling_price * 6.0)/100.0
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1.0,
                        "price_unit" : 100.0
                    })
                ]
            }
        )
        return res
