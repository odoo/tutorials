# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    source_order_line_id = fields.Many2one(
        comodel_name="sale.order.line",
        string="Source Order Line", ondelete="cascade",
    )

    def write(self, vals):
        res = super().write(vals)
        if "price_unit" in vals:
            source_lines = self.filtered(lambda l: not l.source_order_line_id)
            warranty_lines = self.env["sale.order.line"].search([
                ("source_order_line_id", "in", source_lines.ids)
            ])

            configs = self.env["product.warranty.config"].search([
                ("product_id", "in", warranty_lines.mapped("product_id").ids)
            ]).mapped(lambda c: (c.product_id.id, c))
            config_map = dict(configs)

            for wl in warranty_lines:
                source = wl.source_order_line_id
                config = config_map.get(wl.product_id.id)
                if source in source_lines and config:
                    wl.price_unit = source.price_unit * (config.percentage / 100.0)
        return res
