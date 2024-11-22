from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_set_sold(self):
        self.check_access('update')
        self.env['account.move'].sudo().create({
            'partner_id': self.partner_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids':
                [
                    Command.create({
                        'name': self.name,
                        'price_unit': 0.06 * self.selling_price,
                        'quantity': 1
                    }),
                    Command.create({
                        'name': 'administrative fees',
                        'price_unit': 100,
                        'quantity': 1
                    })
                ],
        })
        return super().action_set_sold()
