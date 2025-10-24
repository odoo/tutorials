from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        super().action_sold()
        for prop in self:
            self.env['account.move'].sudo().create(
                {
                    'partner_id': prop.buyer_id.id,
                    'move_type': 'out_invoice',
                    'invoice_line_ids': [
                        Command.create({
                            "name": prop.name,
                            "quantity": 1,
                            "price_unit": prop.selling_price * 0.06,
                        }),
                        Command.create({
                            "name": "Administrative Fee",
                            "quantity": 1,
                            "price_unit": 100,
                        })
                    ]
                }
            )
