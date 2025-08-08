from odoo import models, Command

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def sold_property(self):
        for record in self:
            if record.state != 'offer accepted':
                raise UserWarning('Only accepted offers can be sold.')

            invoice_vals = {'partner_id': record.buyer_id.id,
             'move_type': 'out_invoice',
             'invoice_line_ids': [
                    Command.create({
                        'name': 'Sell commission',
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'Fees',
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                ],}
            self.env['account.move'].create(invoice_vals)
            record.state = 'sold'
        return super().sold_property()
