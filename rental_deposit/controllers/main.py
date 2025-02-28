from odoo.http import request, route
from odoo.addons.website_sale.controllers.variant import WebsiteSaleVariantController

class WebsiteSaleRentingVariantController(WebsiteSaleVariantController):

    @route('/website_sale/get_combination_info', type='json', auth='public', methods=['POST'], website=True)
    def get_combination_info_website(
        self, product_template_id, product_id, combination, add_qty, parent_combination=None,
        **kwargs
    ):
        combination_info = super().get_combination_info_website(product_template_id, product_id, combination, add_qty, parent_combination=None, **kwargs)
        combination_info['add_qty'] = add_qty
        print(combination_info)
        return combination_info
