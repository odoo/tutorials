from odoo import api, fields, models
from odoo import Command
import logging

_logger = logging.getLogger(__name__)

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        _logger.info("ZZZZZ")
        res = super().action_sold()
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)

        for record in self:
          invoice_values = {
            'move_type': 'out_invoice',
            'partner_id': record.buyer_id.id,
            'journal_id': journal.id,
            'invoice_line_ids': [
                Command.create({
                    'name': 'administrative fees',
                    'quantity': 1.0,
                    'price_unit': 100.0,
                }),
                Command.create({
                    'name': 'sold property',
                    'quantity': 1.0,
                    'price_unit': record.selling_price * 0.06,
                })
            ]
          }




          self.env['account.move'].create([invoice_values])

        return res
