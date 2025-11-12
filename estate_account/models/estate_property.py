from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    invoice_created = fields.Boolean(string="Invoice Created", default=False)

    def action_sold(self):
        res = super(EstateProperty, self).action_sold()
        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        for property in self:
            self.env['account.move'].create({
                  'move_type': 'out_invoice',
                  'partner_id': property.buyer_id.id,
                  'journal_id': journal.id,
                  'invoice_date': fields.Date.today(),
                  'invoice_line_ids': [
                      (0, 0, {
                          'name': "Property Sale Commission (6%)",
                          'quantity': 1,
                          'price_unit': property.price * 0.06 #commission_amount
                      }),
                      (0, 0, {
                          'name': "Administrative Fees",
                          'quantity': 1,
                          'price_unit': 100.00 #admin_fee
                      }),
                    ]
            })
            property.invoice_created = True
        return res
