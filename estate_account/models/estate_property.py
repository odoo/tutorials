from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_mark_as_sold(self):
        invoice_vals = {
            'partner_id': self.salesperson_id.id,
            'move_type': 'out_receipt',
            'invoice_line_ids': [
                Command.create(
                    {'name': 'Administrative Fees', 'quantity': 1, 'price_unit': 100.0}
                ),
                Command.create(
                    {'name': 'Down Payment', 'quantity': 1, 'price_unit': 0.06 * self.selling_price}
                ),
            ],
        }
        self.env['account.move'].create(invoice_vals)
        return super().action_mark_as_sold()
