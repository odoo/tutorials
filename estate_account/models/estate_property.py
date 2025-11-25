from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        res = super().action_sold()

        AccountMove = self.env['account.move']
        Journal = self.env['account.journal']
        for prop in self:
            partner = prop.buyer_id
            if not partner:
                continue
            journal = Journal.search([('type', '=', 'sale')], limit=1)
            commission_amount = 0.0
            if prop.selling_price:
                commission_amount = round(0.06 * float(prop.selling_price), 2)
            vals = {
                'partner_id': partner.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create(
                        {
                            'name': 'Commission (6%)',
                            'quantity': 1.0,
                            'price_unit': commission_amount,
                        }
                    ),
                    Command.create(
                        {
                            'name': 'Administrative fees',
                            'quantity': 1.0,
                            'price_unit': 100.00,
                        }
                    ),
                ],
            }
            if journal:
                vals['journal_id'] = journal.id
            AccountMove.create(vals)
        return res
