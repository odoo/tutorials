from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    seller_id = fields.Many2one("res.partner", domain=["is_seller", "=", True])
    parent_order_id = fields.Many2one("sale.order")
    child_order_ids = fields.One2many("sale.order", "parent_order_id")

    def action_confirm(self):

        for order in self:
            if order.parent_order_id:
                continue

            sellers = order.order_line.mapped("product_id.product_tmpl_id.seller_id")

            for seller in sellers:
                seller_line = order.order_line.filtered(
                    lambda line: line.product_id.product_tmpl_id.seller_id == seller
                )

                if not seller_line:
                    continue

                # child_order_vals = {
                #     "partner_id": order.partner_id.id,
                #     "partner_invoice_id": order.partner_invoice_id.id,
                #     "partner_shipping_id": order.partner_shipping_id.id
                #     if order.partner_shipping_id.id
                #     else order.partner_id.id,
                #     "pricelist_id": order.pricelist_id.id,
                #     "origin": order.name,
                #     "parent_order_id": order.id,
                #     "seller_id": seller.id,
                #     "company_id": order.company_id.id,
                # }

                # child_order = self.env["sale.order"].sudo().create(child_order_vals)

                # for line in seller_line:
                #     line.copy(
                #         default={
                #             "order_id": child_order.id,
                #             "seller_id": seller.id,
                #             "company_id": order.company_id.id,
                #         }
                #     )
                # child_order.sudo().action_cancel()

                purchase_order_vals = {
                    "partner_id": seller.id,
                    "origin": order.name,
                    "company_id": order.company_id.id,
                    "date_order": fields.Datetime.now(),
                }

                purchase_order = (
                    self.env["purchase.order"].sudo().create(purchase_order_vals)
                )

                for line in seller_line:
                    po_line_vals = {
                        "order_id": purchase_order.id,
                        "product_id": line.product_id.id,
                        "name": line.name,
                        "product_qty": line.product_uom_qty,
                        "product_uom_id": line.product_uom_id.id,
                        "price_unit": line.price_unit,
                        "date_planned": fields.Datetime.now(),
                    }

                    self.env["purchase.order.line"].sudo().create(po_line_vals)

        return super().action_confirm()
