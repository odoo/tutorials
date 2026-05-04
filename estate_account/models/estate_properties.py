import logging

from odoo import models


_logger = logging.getLogger(__name__)


class EstateProperties(models.BaseModel):
    _inherit = 'estate.properties'

    def property_sold(self):
        # breakpoint()
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.buyer_id.id,  # type: ignore
        }
        # _logger.error(invoice_vals)
        self.env['account.move'].create(invoice_vals)
        return super().property_sold()  # type: ignore
