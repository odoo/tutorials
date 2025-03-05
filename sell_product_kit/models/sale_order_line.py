# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrderline(models.Model):
    _inherit = "sale.order.line"

    is_kit_sale = fields.Boolean(compute="_is_kit", readonly=True, store=True)
    is_sub_product = fields.Boolean(string="Is Sub-Product", default=False)
    parent_line_id = fields.Many2one('sale.order.line', string="Parent Product")
    sub_product_line_ids = fields.One2many('sale.order.line', 'parent_line_id', string="Sub Products")
    is_sub_product = fields.Boolean(string="Is Sub Product", default=False)

    @api.depends('product_id', 'product_id.is_kit')
    def _is_kit(self):
        for record in self:
            record.is_kit_sale = record.product_id.is_kit if record.product_id else False

    def unlink(self):
        sub_products = self.filtered(lambda line: line.is_sub_product)
        if sub_products and not self.env.context.get('allow_sub_product_deletion'):
            if self == sub_products:
                raise models.UserError(_("You cannot delete sub-products individually."))
            return (self - sub_products).unlink()

        sub_lines = self.env['sale.order.line'].search([('parent_line_id', 'in', self.ids)])
        res = super().unlink()
        if res and sub_lines:
            sub_lines.with_context(allow_sub_product_deletion=True).unlink()

        return res
