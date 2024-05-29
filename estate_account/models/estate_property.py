from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        for record in self:
            record.env['account.move'].create(
                {
                    'partner_id': record.buyer_id.id,
                    'move_type': 'out_invoice',
                    'invoice_line_ids': [
                        Command.create({
                            'name': "Downpayment (6% of the selling price)",
                            'quantity': 1,
                            'price_unit': 0.06 * record.selling_price,
                        }),
                        Command.create({
                            'name': "Administrative fees",
                            'quantity': 1,
                            'price_unit': 100
                        })
                    ]
                }
            )
        return super().action_set_sold()
