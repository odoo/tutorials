from odoo import Command, models
from odoo.tools import float_round


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_estate_sold(self):
        result = super().action_estate_sold()

        invoice_vals_list = [
            {
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': self.env._("%(property)s - Commission (6%%)", property=record.name),
                        'quantity': 1,
                        'price_unit': float_round(0.06 * record.selling_price, precision_digits=2),
                    }),
                    Command.create({
                        'name': self.env._("%(property)s - Administrative fees", property=record.name),
                        'quantity': 1,
                        'price_unit': 100.0,
                    }),
                ],
            }
            for record in self
        ]
        self.env['account.move'].create(invoice_vals_list)
        return result
