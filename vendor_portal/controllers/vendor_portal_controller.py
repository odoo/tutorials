# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
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

        all_products = (
            request.env["product.template"].search(domain)
            if domain
            else request.env["product.template"].search([])
        )
        
        total_products = len(all_products)
        total_pages = ceil(total_products / page_size)
        start = (page - 1) * page_size
        end = start + page_size
        filtered_products = all_products[start:end]
        vendors = request.env["res.partner"].search([])
        vendor_countries = vendors.mapped("country_id")
        categories = request.env["product.public.category"].search([])
        products = request.env["product.template"].search([])

        return request.render(
            "vendor_portal.vendor_portal_template",
            {
                "countries": vendor_countries,
                "vendors": vendors,
                "categories": categories,
                "products": products,
                "filtered_products": filtered_products,
                "selected_country": country_id,
                "selected_vendor": vendor_id,
                "selected_category": category_id,
                "selected_product": product_id,
                "current_page": page,
                "total_pages": total_pages,
            },
        )
