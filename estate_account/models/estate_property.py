from odoo import models
from odoo.fields import Command

class Property(models.Model):
    _inherit = "estate.property"

    def _create_invoice(self):
        invoice_vals = {
            "move_type": "out_invoice",
            "partner_id": self.buyer_id.id,
            "line_ids": [
                Command.create({
                    "price_unit": self.selling_price,
                    "quantity": 1,
                    "name": self.name,
                }),
                Command.create({
                    "price_unit": self.selling_price*0.06,
                    "quantity": 1,
                    "name": "Commission",
                }),
                Command.create({
                    "price_unit": 100,
                    "quantity": 1,
                    "name": "Administrative Fees",
                })
            ]
        }

        return invoice_vals

    def action_set_as_sold(self):

        res = super().action_set_as_sold()
        if res is True:
            invoice_vals_list = []
            invoice_vals_list.append(self._create_invoice())
            self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(invoice_vals_list)
        return res
