from odoo import Command, api, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    @api.model_create_multi
    def action_sold(self):
        super().action_sold()
        move = self.env['account.move'].create({
            'move_type' : 'out_invoice',
            'partner_id' : self.buyer_id.id,
            'invoice_line_ids' : [
                Command.create({
                    'name' : self.name,
                    'quantity' : 1,
                    'price_unit' : self.selling_price * 0.06,
                }),
                Command.create({
                    'name' : 'Administrative Fees',
                    'quantity' : 1,
                    'price_unit' : 100,
                })
            ]
        })
