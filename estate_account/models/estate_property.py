from odoo import fields, models, Command
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _inherit = "estate.property"


    def action_property_sold(self):
        res = super().action_property_sold()

        if res:
            for property in self:
                buyer = property.buyer_id

                commission_amount = property.selling_price * 0.06
                admin_fee = 100.00

                invoice_vals = {
                    'partner_id': buyer.id,
                    'move_type': 'out_invoice',
                    "line_ids": [
                        Command.create({
                            'name': property.name,
                            'quantity': 1,
                            'price_unit': property.selling_price,
                        }),
                        Command.create({
                            'name': '6% commission fee',
                            'quantity': 1,
                            'price_unit': commission_amount,
                        }),
                        Command.create({
                            'name': 'Administrative fees',
                            'quantity': 1,
                            'price_unit': admin_fee,
                        })
                    ]
                }

                self.env['account.move'].create(invoice_vals)

        return res
