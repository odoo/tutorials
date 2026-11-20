from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_set_property_sold(self):
        res = super().action_set_property_sold()

        vals_list = []
        for property in self:
            partner_id = property.buyer_id.id
            move_type = 'out_invoice'
            invoice_line_ids = [
                Command.create({
                    'name': property.name,
                    'quantity': 1,
                    'price_unit': property.selling_price * 0.06
                }),
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100.00
                })
            ]
            vals_list.append({
                'partner_id': partner_id,
                'move_type': move_type,
                'invoice_line_ids': invoice_line_ids
                })

        self.env['account.move'].create(vals_list)
        return res
