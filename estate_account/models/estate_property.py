from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def get_sold_property_invoice_values(self):
        return [{
            'partner_id': record.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    'name': "6% of the selling price",
                    'quantity': 1,
                    'price_unit': 0.06 * record.selling_price,
                }),
                Command.create({
                    'name': "Administrative fees",
                    'quantity': 1,
                    'price_unit': 100,
                }),
            ],
        } for record in self]

    def action_property_sold(self):
        invoice_vals = self.get_sold_property_invoice_values()
        self.env['account.move'].create(invoice_vals)

        return super().action_property_sold()
