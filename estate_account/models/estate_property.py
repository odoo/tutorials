from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        for record in self:
            invoice_values = {
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                        Command.create({
                            'name': "Downpayment",
                            'quantity': 1,
                            'price_unit': 0.06 * record.selling_price,
                        }),
                        Command.create({
                            'name': "Administrative Fees",
                            'quantity': 1,
                            'price_unit': 100.00,
                        })
                ]
            }
            self.env['account.move'].create(invoice_values)
        return super(EstateProperty, self).action_set_sold()
