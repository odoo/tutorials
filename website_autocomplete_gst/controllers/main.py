from odoo.exceptions import UserError
from odoo.http import request, route

from odoo.addons.website_sale.controllers import main


class WebsiteSale(main.WebsiteSale):
    @route('/shop/get_data', type='json', auth='public', website=True, sitemap=False)
    def get_company_details(self):
        vat = request.params.get('vat')
        partner = request.env['res.partner']._get_company_details_from_vat(vat)
        return partner if partner else {}

    @route('/shop/update_delivery_address', type='json', auth='public', website=True)
    def update_delivery_address(self, selectedDeliveryAddress, result, **kw):
        field_names = {'name', 'street', 'city', 'country_id', 'phone'}

        order_sudo = request.website.sale_get_order()
        if not order_sudo:
            return
