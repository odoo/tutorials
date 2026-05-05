import logging

from odoo import models
from odoo import Command

_logger = logging.getLogger(__name__)


class EstateProperties(models.BaseModel):
    _inherit = 'estate.properties'

    def property_sold(self):
        breakpoint()
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.buyer_id.id,  # type: ignore
            'invoice_line_ids': [
                Command.create({
                    'name': f'Property: {self.display_name}',
                    'quantity': 1,
                    'price_unit': 0.06 * self.selling_price,  # type: ignore
                }),
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100
                })
            ]
        }
        # _logger.error(invoice_vals)
        self.env['account.move'].create(invoice_vals)
        return super().property_sold()  # type: ignore
