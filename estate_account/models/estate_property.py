from odoo import models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def property_sold_action(self):
        self.env['account.move'].create({
            'partner_id' : self.partner_id.id,
            'move_type' : 'out_invoice',
            'invoice_line_ids': [
                (0, 0, {
                    'name': self.name,
                    'quantity': 1, 
                    'price_unit': self.selling_price * 0.06,
                }),
                (0, 0, {
                    'name': 'administrative fees',
                    'quantity': 1, 
                    'price_unit': 100,
                }),
            ],
        })
        return super().property_sold_action()
