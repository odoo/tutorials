from odoo import Command, api, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        res =  super().action_sold()
        if not self.buyer_id:
            raise UserError("A buyer must be specified before selling the property.")
        
        journal = self.env['account.journal'].search([('type', '=', 'sale')],limit = 1)
        if not journal:
            raise UserError("No sales journal found.")

        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'journal_id': journal.id,
            "invoice_line_ids": [
                Command.create({
                    "name": "Commission (6%)",
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06,
                }),
                Command.create({
                    "name": "Administrative Fees",
                    "quantity": 1,
                    "price_unit": 100.00,
                }),
            ],
        })
        return res
