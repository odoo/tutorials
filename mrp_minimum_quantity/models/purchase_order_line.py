# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    sale_order_line_id = fields.Many2one(comodel_name="sale.order.line", help="Related sale order line for MTO route")

    @api.model
    def _prepare_purchase_order_line_from_procurement(self, product_id, product_qty, product_uom, location_dest_id, name, origin, company_id, values, po):
        res = super()._prepare_purchase_order_line_from_procurement(
            product_id, product_qty, product_uom, location_dest_id, name, origin, company_id, values, po
        )
        sale_order_line = self.env["sale.order.line"].search([
            ("order_id.name", "=", origin),
            ("product_id", "=", product_id.id),
            ("product_uom_qty", "=", product_qty)
        ], limit=1)
        if sale_order_line:
            res["price_unit"] = sale_order_line.price_unit
            res["sale_order_line_id"] = sale_order_line.id
        return res
