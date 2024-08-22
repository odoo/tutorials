from odoo import models, api, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    @api.model
    def action_sold(self):
        # Create an invoice with two lines
        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,  # Assuming 'buyer_id' is the field holding the customer
            'move_type': 'out_invoice',      # 'Customer Invoice'
            'invoice_line_ids': [
                Command.create({
                    'name': 'Property Sale Commission',
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,  # 6% of the selling price
                }),
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100.00,  # Fixed administrative fee
                })
            ],
        })

        # Call the original action_sold method
        return super().action_sold()
