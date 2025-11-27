from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_property_sold(self):
        if self.state == 'offer_accepted' and self.buyer_id:
            invoice_vals = {
                    'move_type': 'out_invoice',
                    'partner_id': self.buyer_id.id,
                    'invoice_line_ids': [
                        Command.create({
                            "name": "Commission 6%",
                            "quantity": 1,
                            "price_unit": self.selling_price * 0.06,
                        }),
                        Command.create({
                            "name": "Administrative fees",
                            "quantity": 1,
                            "price_unit": 100.,
                        }),
                    ],
                }
            self.env['account.move'].sudo().create(invoice_vals)
        return super().action_property_sold()
