from odoo import models
from odoo.fields import Command


class EstateProperty(models.Model):
    _name = 'estate.property'
    _inherit = ["estate.property"]

    # ACTIONS

    def action_set_status_sold(self):
        result = super().action_set_status_sold()

        for record in self:
            self.env["account.move"].create({
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'line_ids': [
                    Command.create({'name': '6% of the selling price', 'quantity': 1, 'price_unit': 0.06 * record.selling_price}),
                    Command.create({'name': 'administrative fees', 'quantity': 1, 'price_unit': 100}),
                ]
            })

        return result
