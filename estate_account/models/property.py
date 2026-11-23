from typing import TYPE_CHECKING

from odoo import fields, models
from odoo.tools import float_utils

if TYPE_CHECKING:
    from estate.models.property import (
        Property as BaseProperty,
    )
else:
    BaseProperty = models.Model


class Property(BaseProperty):
    _inherit = 'estate.property'

    def action_sold(self) -> bool:
        invoice_line_values = [
            {
                'name': 'Commission (6% of sale price)',
                'price_unit': float_utils.float_round(
                    .06 * self.selling_price,
                    precision_rounding=.01,
                ),
                'quantity': 1,
            },
            {
                'name': 'Administrative fees (100€)',
                'price_unit': 100,
                'quantity': 1,
            },
        ]
        order_values = {
            'move_type': 'out_invoice',
            'partner_id': self.buyer_id.id,
            'invoice_line_ids': [
                fields.Command.create(invoice_line_value)
                for invoice_line_value in invoice_line_values
            ],
        }
        self.env['account.move'].create(order_values)
        return super().action_sold()
