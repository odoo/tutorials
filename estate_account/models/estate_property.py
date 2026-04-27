from odoo import models
from odoo import Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for record in self:
            self.env['account.move'].create({
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': record.name,
                        'quantity': 1,
                        'price_unit': record.selling_price,
                    }),
                    Command.create({
                        'name': f'Commission (6%) on {record.name}',
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100.0,
                    })
                ],
            })
        return super().action_sold()
