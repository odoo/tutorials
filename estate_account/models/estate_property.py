from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_property_sold(self):
        res = super().action_property_sold()
        for property in self:
            vals = {
                'partner_id': property.partner_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': property.name,
                        'quantity': 1,
                        'price_unit': property.selling_price * 0.06
                    }),
                    Command.create({
                        'name': "Administrative fees",
                        'quantity': 1,
                        'price_unit': 100
                    }),
                ]
            }
            self.env['account.move'].create(vals)
        return res
