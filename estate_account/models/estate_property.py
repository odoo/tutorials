from odoo import Command, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        self.check_access('write')
        journal = self.env['account.journal'].sudo().search([
            ('type', '=', 'sale'),
        ], limit=1)

        if not journal:
            raise UserError("No sales journal found!")

        for property in self:
            if not property.buyer:
                raise UserError("Buyer is required to create invoice.")

            selling_price = property.selling_price
            service_fee = selling_price * 0.06

            invoice_vals = {
                'partner_id': property.buyer.id,
                'move_type': 'out_invoice',
                'journal_id': journal.id,
                'invoice_line_ids': [
                    Command.create({
                        'name': "Service Fees (6%)",
                        'quantity': 1,
                        'price_unit': service_fee,
                    }),
                    Command.create({
                        'name': "Administrative Fees",
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                ],
            }
            self.env['account.move'].sudo().create(invoice_vals)
        return super().action_sold()
