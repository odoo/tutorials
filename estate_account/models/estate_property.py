from odoo import Command, models

class EstateAccountPropertyModel(models.Model):
    _inherit = 'estate.property'

    def action_sell_property(self):
        for record in self:
            price = super().selling_price
            self.env['account.move'].create({'partner_id': record.buyer,
                                             'move_type': 'customer_invoice',
                                             'invoice_line_ids': [Command.create({'name': super().name + ' commission',
                                                                                  'quantity': 1,
                                                                                  'price_unit': price * 0.06}),
                                                                  Command.create({'name': super().name + ' administrative fees',
                                                                                  'quantity': 1,
                                                                                  'price_unit': 100.0}),
                                                                  ]})
        return super()
