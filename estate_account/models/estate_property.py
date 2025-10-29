from odoo import Command, models


class EstateProperty (models.Model):
    _name="estate.property"
    _inherit = ["estate.property"]

    def action_mark_as_sold(self):
        self.ensure_one()
        res = super().action_mark_as_sold()
        self.env["account.move"].create({
            "line_ids": [
                Command.create({
                    "name": "Accompte",
                    "quantity": "1",
                    "price_unit": self.selling_price * 0.06
                }),
                 Command.create({
                   "name": "Frais administratifs",
                    "quantity": "1",
                    "price_unit": 100
                })
            ],
            'partner_id': self.buyer.id,
            'move_type': 'out_invoice',
        })
        return res
