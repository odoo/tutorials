from odoo import models, Command


class EstatePropertyInherited(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        super().action_set_sold()
        self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.buyer_id.id,
            'invoice_line_ids': [
                Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06
                }),
                Command.create({
                    'name': 'Administrative fees',
                    'quantity': 1,
                    'price_unit': 100.00
                })
            ],
        })
