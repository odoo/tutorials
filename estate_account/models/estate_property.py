from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        super().action_sold()

        for record in self:
            selling_price = record.selling_price or 0.0
            commission_amount = selling_price * 0.06
            self.check_access_rights('write')
            self.check_access_rule('write')
            self.env["account.move"].sudo().create({
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': ('Commission for selling property %s') % record.name,
                        'quantity': 1,
                        'price_unit': commission_amount
                    }),
                    Command.create({
                        'name': ('Administrative Fees'),
                        'quantity': 1,
                        'price_unit': 100.0
                    })
                ],
            })
        return True
