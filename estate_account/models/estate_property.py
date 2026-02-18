from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_set_sold(self):
        partner_id = self.buyer_id.id
        move_type = 'out_invoice'
        property_fee_invoice = {'name': self.name, 'quantity': 1, 'price_unit': self.selling_price * 0.06}
        adminstration_fee_invoice = {
            'name': "Administration fees",
            'quantity': 1,
            'price_unit': 100,
        }

        self.env['account.move'].create({
            'move_type': move_type,
            'partner_id': partner_id,
            "line_ids": [
                Command.create(property_fee_invoice),
                Command.create(adminstration_fee_invoice),
            ]
        })

        return super().action_set_sold()
