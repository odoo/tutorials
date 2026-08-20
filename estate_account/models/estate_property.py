from odoo import Command, models


class InheritedModel(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for property in self:
            self.env['account.move'].create({
                'partner_id': property.buyer_id.id,
                'move_type': 'out_invoice',
                'line_ids': [
                    Command.create({
                        'name': f"Property: {property.name}",  # Prob should use _(%d) for translating, but its just a demo ¯\_(ツ)_/¯
                        'quantity': 1,
                        'price_unit': .06 * property.selling_price,
                    }),
                    Command.create({
                        'name': "Administrative fees",
                        'quantity': 1,
                        'price_unit': 100,
                    }),
                ],
            })

        return super().action_sold()
