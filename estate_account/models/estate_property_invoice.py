from odoo import models, fields


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        """Override the action_sold method to create an invoice when a property is sold."""
        res = super().action_sold()

        # Create an invoice when the property is sold
        move_vals = {
            'partner_id': self.buyer_id.id,  # The customer receiving the invoice
            'move_type': 'out_invoice',  # Customer invoice
            'invoice_line_ids': [(0, 0, {
                'name': f'Sale of property {self.name}',  # Invoice line description
                'quantity': 1,  # Selling one property
                'price_unit': self.selling_price,  # Invoice amount is the selling price
            })]
        }
        self.env['account.move'].create(move_vals)
        return res
