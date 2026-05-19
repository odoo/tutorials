from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        for record in self:
            values = {
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                "line_ids": [
                    Command.create({
                        "name": "6% of the selling price",
                        "quantity": 1,
                        "price_unit": record.selling_price * .06,
                    }),
                    Command.create({
                        "name": "administrative fees",
                        "quantity": 1,
                        "price_unit": 100,
                    }),
                ],
            }
            self.env['account.move'].create(values)
        return super().action_set_sold()
