from odoo import models, Command
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        old = super().action_sold()
        for record in self:

            if not record.buyer_id:
                raise UserError("Cannot sell a property without an assigned buyer.")

            self.env['account.move'].with_context(default_move_type='out_invoice').create({
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': f'Property: {record.name}',
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'Administrative fees',
                        'quantity': 1,
                        'price_unit': 100,
                    })
                ]
            })
        return old
