from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_property_sold(self):
        invoice_vals = {
            'partner_id': self.buyer_id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    'name': "6% of the selling price",
                    'quantity': 1,
                    'price_unit': 0.06 * self.selling_price,
                }),
                Command.create({
                    'name': "Administrative fees",
                    'quantity': 1,
                    'price_unit': 100,
                }),
            ],
        }

        self.env['account.move'].create(invoice_vals)

        return super().action_property_sold()
