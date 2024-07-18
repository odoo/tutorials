from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold_property(self):
        self.env['account.move'].check_access_rights('write')
        self.check_access_rule('write')
        for record in self:
            self.env['account.move'].sudo().create({
                'partner_id': record.partner_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': record.name,
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.07
                    }),
                    Command.create({
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100
                    })
                ]
            })
        return super().action_set_sold_property()
