from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import http

class WebsiteSaleExtended(WebsiteSale):

    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>',
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        response = super().shop(page, category, search, min_price, max_price, ppg, **post)

        if response.qcontext.get('products'):
            for product in response.qcontext['products']:
                product._get_ribbon({})  

        return response
