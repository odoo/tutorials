import typing

from odoo import fields, models

if typing.TYPE_CHECKING:
    from odoo.addons.base.models.res_company import ResCompany
    from odoo.addons.base.models.res_currency import ResCurrency

    from estate.models.property import Property as BaseProperty

else:
    BaseProperty = models.Model


class Property(BaseProperty):
    _inherit = 'estate.property'

    def action_sold(self) -> bool:
        order_values = {
            'move_type': 'out_invoice',
            'partner_id': self.buyer_id.id,
            'invoice_line_ids': [
                fields.Command.create(invoice_line_value)
                for invoice_line_value in self._make_invoice_lines()
            ],
        }
        self.env['account.move'].create(order_values)
        return super().action_sold()

    def _make_invoice_lines(self) -> list[dict[str, typing.Any]]:
        company = typing.cast('ResCompany', self.env.company)
        currency = typing.cast('ResCurrency', company.currency_id)
        return [
            {
                'name': 'Commission (6% of sale price)',
                'price_unit': currency.round(.06 * self.selling_price),
                'quantity': 1,
            },
            {
                'name': 'Administrative fees (100€)',
                'price_unit': 100,
                'quantity': 1,
            },
        ]
