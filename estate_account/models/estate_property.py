from odoo import models, Command
from odoo.tools import float_round

ADMIN_FEE_AMOUNT = 100.00


class EstateProperty(models.Model):
    _inherit = ['estate.property']

    def action_set_state_sold(self):
        for record in self:
            self.env['account.move'].sudo().create(record._prepare_invoice())
        return super().action_set_state_sold()

    def _prepare_invoice(self):
        return {
                'partner_id': self.buyer_id.id,
                'move_type': 'out_invoice',
                "line_ids": [
                    Command.create({
                        "name": "6% of the Selling price",
                        "quantity": 1,
                        'price_unit': self.selling_price * 0.06
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1,
                        'price_unit': ADMIN_FEE_AMOUNT
                    })
                ],
        }
