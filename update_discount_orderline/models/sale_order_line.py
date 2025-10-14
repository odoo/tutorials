from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    is_discount_line = fields.Boolean()
    discount_precentage = fields.Float(string="Percentage")

    def unlink(self):
        orders = self.mapped("order_id")
        res = super().unlink()
        for order in orders:
            order_lines = order.order_line.filtered(lambda l: not l.is_discount_line)
            discount_line = order.order_line.filtered(lambda l: l.is_discount_line)
            if not order_lines:
                order.order_line.unlink()
            elif discount_line:
                discount_line.price_unit = order.updated_discount_amount()
        return res

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        orders = res.mapped("order_id")
        for order in orders:
            discount_line = order.order_line.filtered(lambda l: l.is_discount_line)
            if discount_line:
                discount_line.price_unit = order.updated_discount_amount()
        return res

    def write(self, vals):
        if any(self.mapped("is_discount_line")):
            return super().write(vals)
        res = super().write(vals)
        orders = self.mapped("order_id")
        for order in orders:
            discount_line = order.order_line.filtered(lambda l: l.is_discount_line)
            if discount_line:
                discount_line.price_unit = order.updated_discount_amount()
        return res
