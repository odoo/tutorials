from odoo import models, Command
from odoo.exceptions import AccessError


class EstateProperty(models.Model):

    _inherit = 'estate.property'

    def action_property_sold(self):

        if not self.env['account.move'].check_access_rights('create'):
            try:
                self.check_access_rights('write')
                self.check_access_rule('write')
            except AccessError:
                return self.env['account.move']

        values = []
        for rec in self:

            income_account = self.env['account.account'].search([
                ('account_type', '=', 'income'),
            ], limit=1)
            values.append({
                'name': rec.name + "Invoice",
                'move_type': 'out_invoice',
                'partner_id': rec.buyer_id.id,
                'invoice_line_ids': [
                    Command.create({
                        'name': f'{rec.name}',
                        'quantity': 1,
                        'price_unit': rec.selling_price * 0.06 + rec.selling_price,
                        'account_id': income_account.id
                    })
                ]
            })

        self.env['account.move'].sudo().create(values)
        return super().action_property_sold()
