import logging

from odoo import Command, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        res = super().action_sold()
        _logger.info("================calling sold action=============")
        for record in self:
            if not record.buyer_id:
                raise UserError(_("Property '%s' has no buyer. "
                                  "Please accept an offer before marking as sold.", record.name))

            self.env['account.move'].create({
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                # 'delivery_date': record.offer_ids.date_deadline,

                'invoice_line_ids': [
                    Command.create({
                        'name': f"Commission 6%% — {record.name}",
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    }),

                    Command.create({
                        'name': 'Administrative fees',
                        'quantity': 1,
                        'price_unit': 100.0,
                    }),

                ],
            })
        return res
