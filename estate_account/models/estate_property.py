# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, models


class EstatePropertyAccount(models.Model):
  _inherit = 'estate.property'

  def action_set_property_sold(self):
    self.check_access_rights('write')
    self.check_access_rule('write')

    journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)

    for record in self:
      self.env['account.move'].create({
      'partner_id': record.buyer_id.id,
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
          'price_unit': '100.00'
        })
      ]
    })

    return super().action_set_property_sold()

