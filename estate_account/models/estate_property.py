from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sold_property(self):
        values = []
        for estate in self:
            values.append(
                {
                    'partner_id': estate.buyer_id.id,
                    'move_type': 'out_invoice',
                    'invoice_line_ids': [
                        Command.create({
                            "name": estate.name,
                            "quantity": 0.06,
                            "price_unit": estate.selling_price,
                        }),
                        Command.create({
                            "name": "Administrative fees",
                            "quantity": 1,
                            "price_unit": 100,
                        })
                    ]
                }
            )
        self.env['account.move'].create(values)
        return super().sold_property()
