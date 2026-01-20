import re
from odoo import api, fields, models


class SaleOrderLineInherit(models.Model):
    _inherit = "sale.order.line"

    is_global_discount_line = fields.Boolean(default=False)
    discount_percentage = fields.Float()

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for line in res:
            if "%" in line.name:
                match = re.search(r"(\d+(?:\.\d+)?)%", line.name)
                if match:
                    value = float(match.group(1))
                    line.discount_percentage = value
                line.is_global_discount_line = True
            else:
                line.order_id.recalculate_discount()
        return res

    def write(self, vals):
        if self.env.context.get("skip_recalculate_discount"):
            return super().write(vals)

        res = super().write(vals)

        for line in self:
            line.order_id.with_context(
                skip_recalculate_discount=True
            ).recalculate_discount()
        return res

    def unlink(self):
        orders = self.filtered(lambda ol: not ol.is_global_discount_line).mapped(
            "order_id"
        )
        res = super().unlink()
        for order in orders:
            order.recalculate_discount()
        return res
