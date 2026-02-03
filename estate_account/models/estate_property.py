from odoo import models
from odoo.orm.commands import Command


class EstateAccount(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        # print("override")
        res = super().action_sold()

        for record in self:
            self.env['account.move'].create({
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': record.name,
                        'quantity': 1.0,
                        'price_unit': record.selling_price * 6.0 / 100.0,
                    }),
                    Command.create({
                        'name': "Additional Administrative Fees",
                        'quantity': 1.0,
                        'price_unit': 100.00,
                    })
                ]
            })
        return res
