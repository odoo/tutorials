from odoo import api, models
from odoo.orm.commands import Command


class InheritedEstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_property_sold(self):
        self.env['account.move'].create(
            {
                'partner_id': self.buyer_id.id,
                'move_type': 'out_invoice',
                'line_ids': [
                    Command.create(
                        {
                            'name': "selling price commission(6%)",
                            'quantity': 1,
                            'price_unit': self.selling_price * 0.06,
                        }
                    ),
                    Command.create(
                        {
                            'name': "Administrative fees",
                            'quantity': 1,
                            'price_unit': 100,
                        }
                    ),
                ],
            }
        )
        return super().action_property_sold()
