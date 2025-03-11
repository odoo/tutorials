# type: ignore
from odoo import Command,exceptions,models



class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        print("Estate Account: action_sold method overridden!") # debug for correctly calling this action
        if self.buyer_id:
            try:
                invoice = self.env['account.move'].create({
                    'partner_id': self.buyer_id.id,
                    'move_type': 'out_invoice',
                    'journal_id': self.env['account.journal'].search([('type', '=', 'sale')], limit=1).id,
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
                print(f"Invoice Created: {invoice.name}")
            except Exception as e:
                raise exceptions.UserError(f"Error creating invoice: {e}")
        else:
            raise exceptions.UserError("Buyer not set. Cannot create invoice.")
        return super().action_set_sold()
