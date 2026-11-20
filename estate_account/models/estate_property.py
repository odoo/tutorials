from odoo import Command, fields, models
from odoo.exceptions import AccessError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold_property(self):
        for record in self:
            self.env['account.move'].create(
                {
                    'partner_id': record.buyer_id.id,
                    'move_type': 'out_invoice',
                    "line_ids": [
                        Command.create(
                            {
                                "name": "Sale commission",
                                "quantity": 1,
                                "price_unit": 0.06 * record.selling_price,
                            }
                        ),
                        Command.create(
                            {
                                "name": "Administative fees",
                                "quantity": 1,
                                "price_unit": 100,
                            }
                        ),
                    ],
                }
            )
        return super().action_sold_property()
