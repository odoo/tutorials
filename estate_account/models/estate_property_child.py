from odoo import models, Command
from odoo.exceptions import UserError


class EstatePropertyChild(models.Model):
    _inherit = 'estate.property'

    def _get_default_journal(self):
        return self.env['account.journal'].search([
                *self.env['account.journal']._check_company_domain(self.env.company),
                ('type', '=', 'sale'),
            ], limit=1)

    def action_sold(self):
        journal = self._get_default_journal()
        for record in self:
            if record['selling_price'] == 0:
                raise UserError("An offer must be accepted before setting the property as Sold")
            self.env['account.move'].create([{
                'journal_id': journal.id,
                'move_type': 'out_invoice',
                'partner_id': record.buyer_id.id,
                "line_ids": [
                    Command.create({
                            "name": record['name'],
                            "quantity": 1,
                            "price_unit": record['selling_price'] * 0.06,
                        }),
                    Command.create({
                            "name": "Admin fees",
                            "quantity": 1,
                            "price_unit": 100.00,
                        }),
                ],
            }])
        return super().action_sold()
