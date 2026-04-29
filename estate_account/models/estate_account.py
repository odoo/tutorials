from odoo import Command, models
from odoo.tools.float_utils import float_round


class EstateAccount(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):
        invoice_vals_list = []
        for sold_property in self:
            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': sold_property.buyer_id.id,
                'line_ids': [
                    Command.create({
                        'name': "6% of the selling price",
                        'quantity': 1,
                        'price_unit': float_round(sold_property.selling_price * 0.06, precision_digits=2)
                    }),
                    Command.create({
                        'name': "Administrative fees",
                        'quantity': 1,
                        'price_unit': 100.00
                    }),
                ]
            }
            invoice_vals_list.append(invoice_vals)
        self.env['account.move'].create(invoice_vals_list)
        return super().action_sold_property()
