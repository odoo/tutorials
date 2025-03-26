# type: ignore
from odoo import Command, exceptions, models

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        self.check_access('write')
        print(" reached ".center(100, '='))
        # Explicitly check if the user has write access to the property
        

        if not self.buyer_id:
            raise exceptions.UserError("Buyer not set. Cannot create invoice.")

        journal = self.env['account.journal'].sudo().search([('type', '=', 'sale')], limit=1)
        if not journal:
            raise exceptions.UserError("No sales journal found. Please configure one.")

        invoice = self.env['account.move'].sudo().create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'journal_id': journal.id,
            'invoice_line_ids': [
                Command.create({
                    'name': f'Sale of {self.name} (6%)',
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,
                }),
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100.00,
                }),
            ],
        })

        self.status = 'sold'
        return super().action_set_sold()
