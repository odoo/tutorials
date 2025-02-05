from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        for property in self:
            res = super(EstateProperty, self).action_sold()
            commission_amount = property.price * 0.06
            admin_fee = 100.00
            invoice = self.env['account.move'].create({
                  'move_type': 'out_invoice',
                  'partner_id': property.buyer_id.id,
                  'invoice_date': fields.Date.today(),
                  'invoice_line_ids': [
                      (0, 0, {
                          'name': 'Property Sale Commission (6%)',
                          'quantity': 1,
                          'price_unit': commission_amount
                      }),
                      (0, 0, {
                          'name': 'Administrative Fees',
                          'quantity': 1,
                          'price_unit': admin_fee
                      }),
                    ],
            })
            print(f"Invoice created for property {property.name}. Invoice ID: {invoice.id}")
        return res
