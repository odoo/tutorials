# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, http
from odoo.http import request
from math import ceil


class VendorPortal(http.Controller):

    @http.route("/vendor-portal", type="http", auth="public", website=True)
    def vendor_portal(self, **kwargs):
        country_id = kwargs.get("country_id")
        vendor_id = kwargs.get("vendor_id")
        category_id = kwargs.get("category_id")
        product_id = kwargs.get("product_id")
        page = int(kwargs.get("page", 1))
        page_size = 15

        domain = []
        if country_id:
            domain.append(("seller_ids.partner_id.country_id.id", "=", int(country_id)))
        if vendor_id:
            domain.append(("seller_ids.partner_id.id", "=", int(vendor_id)))
        if category_id:
            domain.append(("public_categ_ids.id", "=", int(category_id)))
        if product_id:
            domain.append(("id", "=", int(product_id)))

        ProductTemplate = request.env["product.template"]
        all_products = ProductTemplate.search(domain or [])
        total_products = len(all_products)
        total_pages = ceil(total_products / page_size)
        start = (page - 1) * page_size
        end = start + page_size
        filtered_products = all_products[start:end]

        return request.render(
            "vendor_portal.vendor_portal_template",
            {
                "countries": request.env["res.partner"].search([]).mapped("country_id"),
                "vendors": request.env["res.partner"].search([]),
                "categories": request.env["product.public.category"].search([]),
                "products": ProductTemplate.search([]),
                "filtered_products": filtered_products,
                "selected_country": country_id,
                "selected_vendor": vendor_id,
                "selected_category": category_id,
                "selected_product": product_id,
                "current_page": page,
                "total_pages": total_pages,
            },
        )

    @http.route(
        "/create-purchase-order", type="http", auth="public", website=True, csrf=False
    )
    def create_purchase_order(self, **post):
        product_id = int(post.get("product_id"))
        vendor_id = int(post.get("vendor_id"))
        qty = float(post.get("product_qty", 1.0))

        product = (
            request.env["product.product"]
            .sudo()
            .search([("product_tmpl_id", "=", product_id)], limit=1)
        )

        if not product or not vendor_id:
            return request.redirect("/vendor-portal")

        vendor_price = next(
            (
                seller.price
                for seller in product.product_tmpl_id.seller_ids
                if seller.partner_id.id == vendor_id
            ),
            0.0,
        )

        PurchaseOrder = request.env["purchase.order"].sudo()
        existing_po = PurchaseOrder.search(
            [("partner_id", "=", vendor_id), ("state", "=", "draft")],
            order="create_date desc",
            limit=1,
        )

        order_line_vals = {
            "product_id": product.id,
            "product_qty": qty,
            "price_unit": vendor_price,
            "product_uom": product.uom_po_id.id,
            "name": product.name,
        }

        if existing_po:
            existing_line = existing_po.order_line.filtered(
                lambda line: line.product_id.id == product.id
            )
            if existing_line:
                existing_line.product_qty += qty
            else:
                existing_po.write({"order_line": [Command.create(order_line_vals)]})
        else:
            PurchaseOrder.create(
                {
                    "partner_id": vendor_id,
                    "order_line": [Command.create(order_line_vals)],
                }
            )

        return request.redirect("/vendor-portal?success=1")
