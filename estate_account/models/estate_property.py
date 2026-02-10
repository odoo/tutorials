from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.estate.property"


    def sold_property_action(self):
        res = super().sold_property_action()
        account_model = self.env['account.move']
        for record in self:
            account_obj = account_model.create(
                {
                    'partner_id': record.buyer.id,
                    'move_type': 'out_invoice',
                    'journal_id': self.env['account.journal'].search([('type', '=', 'sale')], limit=1).id,
                }
            )
            account_obj['line_ids'] = [
                Command.create({
                    'name': "Selling Commission",
                    'quantity': 1,
                    'price_unit': self.selling_price * .06,
                    'account_id': account_obj.id,
                }),
                Command.create({
                    'name': "Administrative fees",
                    'quantity': 1,
                    'price_unit': 100.00,
                    'account_id': account_obj.id,
                })
            ]
        return res

        #result = super(EstateProperty, self).sold_property_action()
        #invoices = self.env['account.move'].create(
        #    {
        #        'partner_id': self.buyer.id,
        #        'move_type': 'out_invoice',
        #        'journal_id': self.env['account.journal'].search([('type', '=', 'sale')], limit=1).id,
        #        'line_ids': [
        #            Command.create({
        #                'name': 'Selling Commission',
        #                'quantity': 1,
        #                'price_unit': self.selling_price * .06
        #            }),
        #            Command.create({
        #                'name': 'Administrative fees',
        #                'quantity': 1,
        #                'price_unit': 100.00
        #            })
        #        ]
        #    }
        #)
        #return result
