from datetime import date

from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_property_sold(self):
        result = super().action_property_sold()
        self.create_invoice()
        return result

    def create_invoice(self):
        try:
            self.check_access_rights('write')
            self.check_access_rule('write')
        except:
            raise UserError("You do not have the necessary permissions to sell this property.")

        invoice = self.env['account.move'].sudo().create({
        'partner_id': self.buyer_id.id,
        'move_type': 'out_invoice',
        'name' : f'INV/2025/{self.id}',
        'invoice_date': date.today(),
        'invoice_line_ids': [
            Command.create({'name': "Selling Price", 'quantity': 1, 'price_unit': self.selling_price * 0.06}),
            Command.create({'name': "Administrative Fees", 'quantity': 1, 'price_unit': 100.00}),
            ]
        })
        return invoice
