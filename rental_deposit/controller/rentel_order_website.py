from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request, route


class RentalOrderWebsite(WebsiteSale):

    @route(['/shop/cart'], type='http', auth="public", website=True, sitemap=False)
    def cart(self, access_token=None, revive='', **post):
        order = request.website.sale_get_order()

        if order:
            order._manage_deposit_lines()

        return super().cart(access_token, revive, **post)

    @route(['/shop/cart/update_json'], type='json', auth="public", methods=['POST'], website=True)
    def cart_update_json(
        self, product_id, line_id=None, 
        add_qty=None, set_qty=None, display=True,
        product_custom_attribute_values=None, 
        no_variant_attribute_value_ids=None, **kwargs):

        order = request.website.sale_get_order()

        if order:
            order._manage_deposit_lines()

        return super().cart_update_json(
            product_id, line_id, add_qty, set_qty, display,
            product_custom_attribute_values, 
            no_variant_attribute_value_ids, 
            **kwargs
        )
