# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSaleInherited(WebsiteSale):
    def _prepare_product_values(self, product, category, search, **kwargs):
        vals = super()._prepare_product_values(product, category, search, **kwargs)
        if product.change_qty:
            default_qty = product.change_qty
            if default_qty % 1 == 0:
                default_qty = int(default_qty)
            vals.update({'default_qty': default_qty})
        return vals
