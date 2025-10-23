from odoo import models, Command


class Property(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        super().action_set_sold()
        for property in self:
            self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': property.buyer_id.id,
                'invoice_line_ids': [Command.create({
                    'name': property.name,
                    'quantity': 1,
                    'price_unit': 0.06 * property.selling_price,
                }), Command.create({
                    'name': 'Administrative fees',
                    'quantity': 1,
                    'price_unit': 100.00,
                })],
            })
