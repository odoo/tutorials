import logging

from odoo import models

_logger = logging.getLogger(__name__)


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        self.env['account.move'].create({
                'partner_id': self.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    (0, 0, {
                        'name': 'commission 6% of selling price',
                        'quantity': 1,
                        'price_unit': self.selling_price * 0.06,
                    }),
                    (0, 0, {
                        'name': 'Administrative fees',
                        'quantity': 1,
                        'price_unit': 100,
                    }),
                ],
            })

        _logger.info("Property sold: %s", self.name)
        return super().action_sold()
