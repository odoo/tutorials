from odoo import Command, models
from odoo.exceptions import AccessError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        self._create_invoice()
        return super().action_sold()

    def _create_invoice(self):
        if not self.env['account.move'].check_access_rights('create', False):
            try:
                self.check_access_rights('write')
                self.check_access_rule('write')
            except AccessError:
                return self.env['account.move']

        invoice_vals_list = []
        for record in self:
            invoice_vals_list.append({
                'partner_id': record.property_buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': record.name,
                        'quantity': 1,
                        'price_unit': record.selling_price
                    }),
                    Command.create({
                        'name': "6%",
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06
                    }),
                    Command.create({
                        'name': "Administrative fees",
                        'quantity': 1,
                        'price_unit': 100.0
                    }),
                ]
            })

        moves = self.env['account.move'].sudo().create(invoice_vals_list)

        return moves
