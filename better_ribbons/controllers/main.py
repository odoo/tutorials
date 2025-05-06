from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request, route


class WebsiteSaleExtended(WebsiteSale):
    @route(
        [
            '/shop',
            '/shop/page/<int:page>',
            '/shop/category/<model("product.public.category"):category>',
            '/shop/category/<model("product.public.category"):category>/page/<int:page>',
        ],
        type='http',
        auth='public',
        website=True,
    )
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        response = super().shop(
            page, category, search, min_price, max_price, ppg, **post
        )

        if products := response.qcontext.get('products'):
            products_prices = response.qcontext.get('products_prices')
            for product in products:
                product._set_ribbon(products_prices.get(product.id))

        return response

    @route(
        ['/shop/<model("product.template"):product>'],
        type='http',
        auth='public',
        website=True,
        readonly=True,
    )
    def product(self, product, category='', search='', **kwargs):
        response = super().product(product, category, search, **kwargs)

        if prd := response.qcontext.get('product'):
            prices = prd._get_sales_prices(request.env['website'].get_current_website())
            prd._set_ribbon(prices.get(prd.id))

        return response
