from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_to_sold(self):
        for property in self:
            self.env['account.move'].create(
                {
                    'partner_id': property.buyer_id.id,
                    'move_type': 'out_invoice',
                    'invoice_line_ids': [
                        Command.create({
                            'name': property.name + ' Down Payment',
                            'quantity': 1,
                            'price_unit': property.selling_price * 0.06,
                        }),
                        Command.create({
                            'name': 'Administrative Fee',
                            'quantity': 1,
                            'price_unit': 100,
                        })
                    ]
                })
        return super().action_set_to_sold()
