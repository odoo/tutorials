from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        res = super().action_set_sold()
        self.env['account.move'].sudo().create({
            'partner_id': self.buyer_id.id, 
            'move_type': 'out_invoice', 
            "invoice_line_ids": [
                Command.create({
                    "name": "Property Sale Commission",
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06
                }),
                Command.create({
                    "name": "Administrative Fees",
                    "quantity": 1,
                    "price_unit": 100.00
                }),
            ],
        })
        return res
