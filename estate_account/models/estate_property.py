from odoo import models, Command

class estate_property(models.Model):
    _inherit = 'estate.property'

    def sold_property_button(self):
        res = super().sold_property_button()

        for property in self:
            self.env['account.move'].create({
                'partner_id': property.buyer_id.id,  # corrected field name
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        "name": property.name,
                        "quantity": 1.0,
                        "price_unit": property.selling_price * 6.0 / 100.0,
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1.0,
                        "price_unit": 100.0,
                    }),
                ],
            })

        return res
