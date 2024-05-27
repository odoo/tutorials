from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        for record in self:
            invoice_line_1 = {
                'name': '6%% of selling price',
                'quantity': 1,
                'price_unit': 0.06 * record.selling_price,
            }
            invoice_line_2 = {
                'name': 'Administrative fees',
                'quantity': 1,
                'price_unit': 100.00,
            }
            invoice_vals = {
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create(invoice_line_1),
                    Command.create(invoice_line_2),
                ],
            }
            record.env['account.move'].create(invoice_vals)
        return super().action_set_sold()
