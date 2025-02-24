from odoo import models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        """Override action_sold to create a customer invoice with two invoice lines."""
        self.env['account.move'].check_access('create')
        for property in self:
            self.env['account.move'].create({
                'partner_id': property.buyer_id.id,  # Ensure ID, not a recordset
                'move_type': 'out_invoice',  # Customer Invoice type
                'invoice_line_ids': [
                    (0, 0, {  # First line: 6% of the selling price
                        'name': "Commission (6% of Selling Price)",
                        'quantity': 1,
                        'price_unit': property.selling_price * 0.06,
                    }),
                    (0, 0, {  # Second line: Fixed administrative fee
                        'name': "Administrative Fees",
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                ],
            })
        return super().action_sold()
