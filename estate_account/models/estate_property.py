from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_set_sold(self):
        self.check_access_rights('write')
        self.check_access_rule('write')

        super().action_set_sold()

        for estate in self:
            selling_price = estate.selling_price
            commission = selling_price * 0.06
            # Create the invoice
            # Use sudo() because the user can generate an invoice without the billing access rights.
            self.env['account.move'].sudo().create({
                'name': estate.name,
                'partner_id': estate.buyer_id.id,
                'move_type': 'out_invoice',
                'journal_id': 1,
                'invoice_line_ids': [
                    Command.create({
                        'name': f"Commission for selling property {estate.name}",
                        'quantity': 1,
                        'price_unit': commission
                    }),
                    Command.create({"name": "Administrative Fees",
                                    "quantity": 1,
                                    "price_unit": 100.0,
                                    }),
                ],
            })
        return True
