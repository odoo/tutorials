from odoo import models, Command


class EstatePropertyInherited(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):

        self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create({
            'partner_id': super().buyer_id.id,
            'move_type': 'out_invoice',
            'journal_id': 1,
            "invoice_line_ids": [
                Command.create({
                    "name": super().name,
                    "quantity": 1,
                    "price_unit": super().selling_price * 0.06,
                }),
                Command.create({
                    "name": "fee",
                    "quantity": 1,
                    "price_unit": 100,
                })
            ],
        })
        return super().action_sold()
