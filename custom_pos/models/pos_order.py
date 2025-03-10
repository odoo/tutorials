from odoo import api, models, _
from odoo.exceptions import ValidationError


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    @api.constrains('price_unit')
    def _check_min_price(self):
        for line in self:
            min_price = line.product_id.min_price
            if line.price_unit < min_price:
                raise ValidationError(_('The price of product cannot be lower than the minimum price'))
