from odoo import models, Command
from odoo.exceptions import UserError

class EstateAccount(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        if not journal:
            raise UserError(
                'No Sales Journal found for your company. Create one in Invoicing > Configuration > Journals.')
        
        for record in self:
            invoice = {'partner_id': record.buyer_id.id,
                        'move_type': 'out_invoice',
                        'journal_id': journal.id,
                        'line_ids': [
                            Command.create({
                                'name': record.name,
                                'quantity': 1,
                                'price_unit': record.selling_price * 0.06,
                            }),
                            Command.create({
                                'name': 'Fixed fees',
                                'quantity': 1,
                                'price_unit': 100.00, 
                            })
                        ]}
            self.env['account.move'].create(invoice)
        return super().action_sold()
