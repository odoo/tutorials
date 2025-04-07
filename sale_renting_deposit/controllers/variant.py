# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.http import request, route

from odoo.addons.website_sale.controllers.variant import WebsiteSaleVariantController


class SaleRentingDepositVariantController(WebsiteSaleVariantController):

    @route()
    def get_combination_info_website(self, *args, **kwargs):
        res = super().get_combination_info_website(*args, **kwargs)
        quantity = kwargs.get('add_qty', 1)
        deposit_amount = request.env['product.product'].browse(res['product_id']).deposit_amount
        res['deposit_amount'] = deposit_amount
        res['total_deposit_amount'] = deposit_amount * quantity
        return res
