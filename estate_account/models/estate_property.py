from odoo import api, models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_mark_sold(self):
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
        return super().action_mark_sold()
