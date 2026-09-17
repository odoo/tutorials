from odoo import Command, models


class EstateInheritedProperty(models.Model):
    _inherit = 'estate.property'

    def sold_property(self):
        journal_id = self.env['account.journal'].search([('code', '=', 'INV')], limit=1).id
        for record in self:
            self.env['account.move'].create({
                'partner_id': record.buyer.id,
                'move_type': 'out_invoice',
                'journal_id': journal_id,
                'invoice_line_ids': [
                    Command.create({
                        'name': self.env._('Purchase of %s', record.id),
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': self.env._('Administrative fees'),
                        'quantity': 1,
                        'price_unit': 100,
                    }),
                ],
            })
        return super().sold_property()
