from odoo import Command, models

class EstatePropertyAccount(models.Model):
  _inherit = "estate_model"

  def sold_action(self):
    journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)

    for record in self:
      self.env["account.move"].create({
      'partner_id': record.buyer.id,
      'move_type': 'out_invoice',
      'journal_id': journal.id,
      'invoice_line_ids': [
        Command.create({
          'name': record.name,
          'quantity': 1,
          'price_unit': record.selling_price * 0.06
        }),
        Command.create({
          'name': 'Administrative Fees',
          'quantity': 1,
          'price_unit': "100.00"
        })
      ]
    })
    return super().sold_action()