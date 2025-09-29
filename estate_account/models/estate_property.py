from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def _prepare_invoice(self):
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.buyer_id.id,
            'invoice_line_ids': [
                Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price,
                }),
                Command.create({
                    'name': "Taxes and Death",
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,
                }),
                Command.create({
                    'name': "Administrative fees",
                    'quantity': 1,
                    'price_unit': 100.0,
                }),
            ],
        }
        return invoice_vals

    def action_set_sold(self):
        invoice_vals_list = []
        for property in self:
            invoice_vals = property._prepare_invoice()
            invoice_vals_list.append(invoice_vals)

        self.env['account.move'].sudo().create(invoice_vals_list)

        return super().action_set_sold()
