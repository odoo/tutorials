from odoo import models


class EstateProperty(models.Model):
    _inherit = ["estate.property"]
    _name = 'estate.property'

    # -------------------------------------------------------------
    # Inherited actions
    # -------------------------------------------------------------
    def action_flag_property_as_sold(self):
        for record in self:
            invoice_vals = {
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                "invoice_line_ids": [(0, 0, {
                    "name": "Property sold :'" + record.name + "'",
                    "quantity": 1,
                    "price_unit": (0.06 * record.selling_price),
                }), (0, 0, {
                    "name": "Administrative Fees",
                    "quantity": 1,
                    "price_unit": 100.00,

                })]
            }
            self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(invoice_vals)
        return super().action_flag_property_as_sold()
