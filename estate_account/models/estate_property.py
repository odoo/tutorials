# Imports of odoo
from odoo import Command, models


class InheritedEstateProperty(models.Model):
    # === Private attributes ===
    _inherit = 'estate.property'

    # === Action methods ===
    def action_mark_sold(self):
        """When a property is marked as sold,
        this method creates a customer invoice.

        The invoice contains two lines:
        - Selling price of the property.
        - 6% of the selling price as commission.
        - A flat administrative fee of ₹100.
        """
        res = super().action_mark_sold()

        for property in self:
            if property.buyer_id:
                invoice_vals = {
                    'partner_id': super().buyer_id.id,
                    'move_type': 'out_invoice',
                    'invoice_line_ids': [
                        Command.create({
                            'name': 'Selling Price',
                            'quantity': 1,
                            'price_unit': property.selling_price,
                        }),
                        Command.create({
                            'name': 'Selling Price (6%)',
                            'quantity': 1,
                            'price_unit': property.selling_price * 0.06,
                        }),
                        Command.create({
                            'name': 'Administrative Fees',
                            'quantity': 1,
                            'price_unit': 100.00,
                        })
                    ]
                }

                self.env['account.move'].sudo().with_context(
                    default_move_type='out_invoice').create(invoice_vals)
        return res
