from odoo import fields, models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):
        res = super().action_sold_property()
        for record in self:
            self.env['account.move'].create({
                'partner_id': self.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({
                        "name": record.name,
                        "quantity": 1,
                        "price_unit": record.selling_price * 0.6
                    }),
                    Command.create({
                        "name": record.name,
                        "quantity": 1,
                        "price_unit": "100.00"
                    })
                ]
                })
        return res
