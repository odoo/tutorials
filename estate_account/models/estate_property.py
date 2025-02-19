from datetime import date
from odoo import _, Command, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        result = super().action_set_sold()
        self.create_invoice()
        return result

    def create_invoice(self):
        try:
            self.check_access('write')
            self.check_access('write')
            invoice = self.env['account.move'].sudo().create({
                'partner_id': self.buyer_id.id,
                'move_type': 'out_invoice',
                'name': f'INV/2025/{self.id}',
                'invoice_date': date.today(),
                'invoice_line_ids': [
                    Command.create({
                        'name': "Selling Price",
                        'quantity': 1,
                        'price_unit': self.selling_price * 1.06
                    }),
                    Command.create({
                        'name': "Administrative Fees",
                        'quantity': 1,
                        'price_unit': 100.00
                    }),
                ]
            })
            return invoice
        except Exception as e:
            raise UserError(_("You do not have the necessary permissions to sell this property."))
