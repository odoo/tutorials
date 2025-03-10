# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class CustomWebsiteSale(WebsiteSale):

    @http.route(['/shop/<model("product.template"):product>'], type='http', auth="public", website=True, sitemap=True)
    def product(self, product, category='', search='', **kwargs):
        values = self._prepare_product_values(product, category, search, **kwargs)

        values['ecommerce_extended_description'] = product.ecommerce_extended_description

        return request.render("website_sale.product", values)
