from odoo import models, Command
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def _get_default_journal(self):
        return self.env['account.journal'].search([
            *self.env['account.journal']._check_company_domain(self.env.company),
            ('type', '=', 'sale'),
        ], limit=1)

    def _prepare_invoice_lines(self):
        return [
                    Command.create({
                        'name': 'Selling price - 6%',
                        'quantity': '1',
                        'price_unit': self.selling_price * .06,
                    }),
                    Command.create({
                        'name': 'Administrative fees',
                        'quantity': '1',
                        'price_unit': 100,
                    })
                ]

    def action_sell(self):
        journal = self._get_default_journal()
        if not journal:
            raise UserError("No journal")

        self.env['account.move'].create(
            [{
                'partner_id': self.buyer_id.id,
                'move_type': 'out_invoice',
                'journal_id': journal.id,
                'invoice_line_ids': self._prepare_invoice_lines()
            }])

        return super().action_sell()
