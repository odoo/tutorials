from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):
        for record in self:
            self.env['account.move'].create(
                {
                    'partner_id': int(record.buyer_id),
                    'move_type': 'out_invoice',
                    'invoice_line_ids': [
                        Command.create({
                            'name': f"{record.name} (6% down payment)",
                            'quantity': 1,
                            'price_unit': 0.06 * record.selling_price,
                        }),
                        Command.create({
                            'name': 'Admin fees',
                            'quantity': 1,
                            'price_unit': 100.00,
                        }),
                    ],
                },
            )
        return super().action_sold_property()
