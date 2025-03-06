from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_deposit = fields.Boolean(string="Is Deposit", default=False)

    @api.model_create_multi
    def create(self, vals_list):
        records = super(SaleOrderLine, self).create(vals_list)
        if not self.env.context.get("no_update_deposit"):
            for record in records:
                record.order_id.with_context(
                    no_update_deposit=True
                )._update_deposit_product()
        return records

    def write(self, vals):
        res = super(SaleOrderLine, self).write(vals)
        if not self.env.context.get("no_update_deposit"):
            for record in self:
                record.order_id.with_context(
                    no_update_deposit=True
                )._update_deposit_product()
        return res

    def unlink(self):
        orders = self.mapped("order_id")
        res = super(SaleOrderLine, self).unlink()
        for order in orders:
            order.with_context(no_update_deposit=True)._update_deposit_product()
        return res
