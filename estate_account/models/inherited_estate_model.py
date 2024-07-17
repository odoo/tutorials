from odoo import models, Command


class InheritedEstateModel(models.Model):
    _inherit = 'estate.property'

    def sold(self):
        selling_price = self.selling_price
        account_move = {
            'partner_id': self.buyer_id,
            'move_type': 'out_invoice',
            "line_ids": [
                Command.create({
                    "name": "Selling price",
                    "quantity": 1,
                    "price_unit": selling_price * 0.06
                }),
                Command.create({
                    "name": "administrative fees",
                    "quantity": 1,
                    "price_unit": 100
                }),
            ],
        }
        self._create_invoices(account_move)
        return super().sold()

    def _create_invoices(self, invoice):
        self.env['account.move'].sudo().create(invoice)
