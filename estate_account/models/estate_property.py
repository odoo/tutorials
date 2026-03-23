from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sell(self):

        for property_record in self:
  
            invoice_vals = {
                'name': property_record.name + ' ' +'Invoice', 
                'partner_id': property_record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': 'Property Price',
                        'quantity': 1.0,
                        'price_unit': property_record.selling_price
                    }),
                    Command.create({
                        'name': '6% Commission on Sales',
                        'quantity': 1.0,
                        'price_unit': property_record.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'Administrative Fees',
                        'quantity': 1.0,
                        'price_unit': 100.00,
                    })
                ]
            }

            self.env['account.move'].create(invoice_vals)

        return super().action_sell()
