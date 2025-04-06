from odoo import models, Command

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        journal_id = self.env['account.journal'].search([("type", '=', 'sale')], limit=1)
        invoice_vals_list = []
        for record in self:
            invoice_line_vals = {
                'partner_id': record.buyer_id.id,
                'invoice_user_id': record.sale_id.id,
                'move_type': 'out_invoice',
                'journal_id': journal_id.id,
                'invoice_line_ids': [
                    Command.create({
                        "name": record.name,
                        "quantity": 1,
                        "price_unit": record.selling_price * 0.6,
                    }),
                    Command.create({
                        "name": 'administrative fees',
                        "quantity": 1,
                        "price_unit": 100.00,
                    })
                ]
            }
            invoice_vals_list.append(invoice_line_vals)

        self.env['account.move'].create(invoice_vals_list)
        return super().action_sold()
