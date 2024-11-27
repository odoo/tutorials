
from odoo import models

class estate_property(models.Model):
    _inherit = 'estate.property'

    def action_set_property_as_sold(self):
        for record in self:
            if not record.buyer:
                raise ValueError(("Please set a buyer before selling the property."))

            if not record.selling_price:
                raise ValueError(("Please set a selling price before selling the property."))

            commission_amount = record.selling_price * 0.06
            admin_fee = 100.00

            invoice_values = {
                'partner_id': record.buyer.id,  # Buyer of the property
                'move_type': 'out_invoice',    # Customer Invoice
                'invoice_line_ids': [
                    (0, 0, {
                        'name': ("Commission for selling the property"),
                        'quantity': 1,
                        'price_unit': commission_amount,
                    }),
                    (0, 0, {
                        'name': ("Administrative Fees"),
                        'quantity': 1,
                        'price_unit': admin_fee,
                    }),
                ],
            }

            self.env['account.move'].create(invoice_values)
        return super(estate_property, self).action_set_property_as_sold()