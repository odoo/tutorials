import logging

from odoo import models, Command

_logger = logging.getLogger(__name__)


class EstateSalesOrder(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        for rec in self:
            res = super().action_sold()
            self.env['sale.order'].create({
                'partner_id': rec.buyer_id.id,
                'user_id': rec.salesperson_id.id,
                'order_line': [
                    Command.create({
                        'name': rec.name,
                        'product_uom_qty': 1,
                        'price_unit': rec.selling_price

                    })
                ]
            })

        return res
