from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):
        self.env['account.move'].create(
            {
                'partner_id': self.buyer.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': "6% of the selling price",
                        'quantity': 1,
                        'price_unit': 0.06 * self.selling_price
                    }),
                    Command.create({
                        'name': "administrative fees",
                        'quantity': 1,
                        'price_unit': 100
                    })
                ]
            }
        )
        return super().action_sold_property()
