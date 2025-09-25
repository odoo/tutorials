from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        res = super().action_set_sold()
        sold_properties = self.filtered(lambda property: property.buyer_id)
        if not sold_properties:
            return res

        moves_vals = []
        for property in sold_properties:
            moves_vals.append({
                'partner_id': property.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': '6% of the selling price',
                        'quantity': 1,
                        'price_unit': property.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'Administrative fees',
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                ],
            })

        self.env['account.move'].create(moves_vals)
        return res
