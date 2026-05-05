import logging

from odoo import fields, models
from odoo import Command

_logger = logging.getLogger(__name__)


class EstateProperties(models.BaseModel):
    _inherit = 'estate.properties'

    invoice_count = fields.Integer(compute='')

    
    def _check_admin_fees(self, admin_fees):
        if admin_fees < 100:
            return 100
        elif admin_fees > 500:
            return 500
        else:
            return admin_fees

    def property_sold(self):
        breakpoint()
        super().property_sold()  # type: ignore
        if self.property_type_id.type == 'Apartment':  # type:ignore
            # _logger.error(self.property_type_id.type)  # type:ignore
            admin_fees = 0.02 * self.selling_price  # type: ignore
            # _logger.error(admin_fees)
            admin_fees = self._check_admin_fees(admin_fees)
            # _logger.error(admin_fees)
        elif self.property_type_id.type == 'House':  # type:ignore
            # _logger.error(self.property_type_id.type)  # type:ignore
            admin_fees = 0.03 * self.selling_price  # type: ignore
            # _logger.error(admin_fees)
            admin_fees = self._check_admin_fees(admin_fees)
            # _logger.error(admin_fees)
        else:
            admin_fees = 100
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
                    'price_unit': admin_fees
                })
            ]
        }
        # _logger.error(invoice_vals)
        self.env['account.move'].create(invoice_vals)
        return super()
