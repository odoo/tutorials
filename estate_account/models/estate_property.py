from odoo import Command, models


class Property(models.Model):
    _inherit = "estate.property"

    def sell(self):
        for record in self:
            values = {
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': '6% of the selling price',
                        'quantity': 1,
                        'price_unit': 0.06 * record.selling_price,
                    }),
                    Command.create({
                        'name': 'Administrative fees',
                        'quantity': 1,
                        'price_unit': 100,
                    }),
                ],
            }
            self.env['account.move'].create(values)

        return super().sell()
