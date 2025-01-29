from odoo import models

class EstateProperty(models.Model):
    _name = 'estate.property.account'
    _inherit = 'estate.property'

    def sold_property(self):
        print('aaa')
        for record in self:
            if record.state != 'offer accepted':
                raise ValueError('Only accepted offers can be sold.')

            invoice_vals = {'partner_id': record.buyer_id.id, 'move_type': 'out_invoice'}
            self.env['account.move'].create(invoice_vals)
            record.state = 'sold'
        return super(EstateProperty, self).sold_property()
