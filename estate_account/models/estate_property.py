from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_estate_property_sold(self):
        self.env["account.move"].check_access("create")
        res = super().action_estate_property_sold()
        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create(
                    {'name': self.name, 'quantity': 1, 'price_unit': self.selling_price}
                ),
                Command.create(
                    {'name': "Charges", 'quantity': 1, 'price_unit': self.selling_price * 0.06}
                ),
                Command.create(
                    {'name': "Administrative fees", 'quantity': 1, 'price_unit': 100}
                ),
            ],
        })
        return res
