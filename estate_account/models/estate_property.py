from odoo import api, Command, fields, models
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit = ['estate.property']

    def action_sold(self):
        res = super().action_sold()
        for property in self:
            self.env['account.move'].create({
                'partner_id': property.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': "6% of the selling price",
                        'quantity': 1,
                        'price_unit': 0.06 * property.selling_price,
                    }),
                    Command.create({
                        'name': "administrative fees",
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                ],
            })
        return res
