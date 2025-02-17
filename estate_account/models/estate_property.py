from odoo import Command, fields, models
from odoo.exceptions import UserError, AccessError

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold_button(self):
        # Check if the current user has access rights and rules for updating this property
        try:
            self.check_access_rights('write')
            self.check_access_rule('write')
            print("Access check passed for updating property.")
        except AccessError as e:
            print("Access check failed for updating property:")
            print(str(e))
            raise UserError("You do not have permission to update this property.")
        # Call the original action_sold_button method
        res = super().action_sold_button()
        if not self.buyer_id:
            raise UserError("A buyer must be specified before selling the property.")
        journal = self.env['account.journal'].sudo().search([('type', '=', 'sale')], limit=1)
        if not journal:
            raise UserError("No sales journal found. Please ensure there is a journal of type 'Sale'.")
        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'journal_id': journal.id,
            "invoice_line_ids": [
                Command.create({
                    "name": "Commission (6%)",
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06, # 6% of selling price
                }),
                Command.create({
                    "name": "Administrative Fees",
                    "quantity": 1,
                    "price_unit": 100.00, # Fixed fee
                }),
            ],
        })
        return res
