from odoo import models, fields, _
from odoo.exceptions import ValidationError


class ZeroStock(models.Model):
    _inherit = "sale.order"

    zero_stock_approval = fields.Boolean(string="Approve", default=False)

    def action_confirm(self):
        for record in self:
            if not record.zero_stock_approval:
                for line in record.order_line:
                    if line.product_id.qty_available <= 0:
                        raise ValidationError(_(
                            "You cannot confirm this order because the product has zero stock. "
                            "Please ask a Sales Manager to toggle the 'Zero Stock Approval' checkbox first!")
                        )
        return super().action_confirm()
