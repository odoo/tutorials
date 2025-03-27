from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo import Command


class EstateAccount(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        for property_record in self:
            if property_record.state == 'cancelled':
                raise UserError("A cancelled property cannot be set as sold")

            partner_id = property_record.buyer_id
            selling_price = property_record.selling_price

            invoice_line_1 = Command.create(
                {
                    'name': 'Property Sale',
                    'quantity': 1,
                    'price_unit': selling_price * 1.06,
                },
            )

            invoice_line_2 = Command.create(
                {
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100.00,
                },
            )

            journal_id = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)

            if not journal_id:
                raise UserError("No sale journal found")

            invoice_values = {
                'partner_id': partner_id.id,
                'move_type': 'out_invoice',
                'journal_id': journal_id.id,
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': [invoice_line_1, invoice_line_2],
            }

            self.env['account.move'].create(invoice_values)

        return super().action_sold()
