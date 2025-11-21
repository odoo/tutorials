from odoo import fields, models, Command
from odoo.exceptions import AccessError 

class EstateProperty(models.Model):
    _inherit = "estate.property"
    
    def action_sold_property(self):
        try:
            self.check_access('write')
        except AccessError:
            raise AccessError("You do not have permission to modify this property.")

        print("Access check passed.")
        self.env['account.move'].sudo().create(
            {
                'partner_id': self.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': self.name,
                        'quantity': 1,
                        'price_unit': self.selling_price,
                    }),

                    Command.create({
                        'name': 'Selling Commision is 6%',
                        'quantity': 1,
                        'price_unit': self.selling_price*0.06,
                    }),

                    Command.create({
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100,
                    })
                ]
            }
        )
        return super().action_sold_property()
    