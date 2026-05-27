from odoo import models, Command


class Sales(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        result = super().action_sold()
        for rec in self:
            self.env['sale.order'].create({
                'partner_id': rec.buyer_id.id,
                'order_line': [Command.create({
                    'name': rec.name,
                })]
            })
        return result
