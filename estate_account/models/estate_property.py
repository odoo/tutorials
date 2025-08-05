from odoo import models, Command


class InheritedEstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_property_sold(self):
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': super().buyer.id,
            "invoice_line_ids": [
                Command.create({
                    'name': 'Selling Price (6%)',
                    'quantity': 1,
                    'price_unit': (6 * super().selling_price) / 100
                }),
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100.0,
                }),
            ]
        }
        self.env['account.move'].sudo().with_context(
            default_move_type='out_invoice').create(invoice_vals)
        return super().action_set_property_sold()
