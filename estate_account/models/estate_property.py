from odoo import  Command, models
from odoo.exceptions import UserError


class EstatePropertyInherit(models.Model):
    _inherit = 'estate.property'
    
    def action_property_sold(self):
        res = super().action_property_sold()

        if not self.partner_id:
            raise UserError("A buyer must be specified before selling the property.")

        journal = self.env['account.journal'].search([('type', '=', 'sale')],limit = 1)
        if not journal:
            raise UserError("No sales journal found.")

        self.env['account.move'].sudo().create({
            'partner_id': self.partner_id.id,
            'move_type' : 'out_invoice',
            "invoice_line_ids" : [
                Command.create({
                    "name" : self.name,
                    "quantity" : 1,
                    "price_unit" : self.selling_price,
                })
                ,
                Command.create({
                    "name" : "Commission (6%)",
                    "quantity" : 1,
                    "price_unit" : self.selling_price * 0.06
                }),
                Command.create({
                    "name" : "Administrative Fees",
                    "quantity" : 1,
                    "price_unit" : 100.00
                })
            ]
        })
        return res
