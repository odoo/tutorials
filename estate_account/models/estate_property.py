from odoo import models, Command

# TODO - Separate Command.create() and Invoice
# TODO - utiliser xpath
    # Inside property view => nb invoices
    # More on Command.create/update/etc.


class EstateProperty(models.Model):
    _inherit = "estate.estate.property"


    def sold_property_action(self):
        res = super().sold_property_action()
        account = self.env['account.move']
        for record in self:
            account.create(
                {
                    'partner_id': record.buyer.id,
                    'move_type': 'out_invoice',
                    'journal_id': self.env['account.journal'].search([('type', '=', 'sale')], limit=1).id,
                }
            )
            account['invoice_line_ids'] = [
                (0, 0, {
                    'name': "Selling Commission",
                    'quantity': 1,
                    'price_unit': self.selling_price * .06,
                    'account_id': account.id,
                }),
                (0, 0, {
                    'name': "Administrative fees",
                    'quantity': 1,
                    'price_unit': 100.00,
                    'account_id': account.id,
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
