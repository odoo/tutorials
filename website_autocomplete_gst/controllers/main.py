from odoo.http import request, route
from werkzeug.exceptions import Forbidden

from odoo.addons.website_sale.controllers import main


class WebsiteSale(main.WebsiteSale):
    @route('/shop/get_data', type='json', auth='public', website=True, sitemap=False)
    def get_company_details(self):
        vat = request.params.get('vat')
        partner = request.env['res.partner']._get_company_details_from_vat(vat)
        return partner if partner else {}

    def _get_checkout_page_values(self, **kwargs):
        qcontext = super()._get_checkout_page_values(**kwargs)
        qcontext.pop('use_delivery_as_billing', None)
        return qcontext

    @route('/shop/update_invoice_address', type='json', auth='public', website=True)
    def shop_update_invoice_address(self, address_type='billing', **kw):
        company_data = self.get_company_details()
        if company_data:
            order_sudo = request.website.sale_get_order().sudo()
            if order_sudo:
                #Update the invoice address based on vat
                invoice_address = request.env['res.partner'].sudo().create({
                    'name': company_data.get('name'),
                    'company_type': 'company',
                    'parent_id': False,
                    'street': company_data.get('street'),
                    'street2': company_data.get('street2'),
                    'city': company_data.get('city'),
                    'state_id': company_data.get('state_id'),
                    'country_id': company_data.get('country_id'),
                    'zip': company_data.get('zip'),
                    'vat': company_data.get('vat'),
                })
                partner_fnames = set()
                order_sudo.partner_invoice_id = invoice_address
                ResPartner = request.env['res.partner'].sudo()
                partner_sudo = ResPartner.browse(invoice_address.id).exists()
                if (address_type == 'billing' and partner_sudo != order_sudo.partner_invoice_id):
                   partner_fnames.add('partner_invoice_id')
                order_sudo._update_address(invoice_address.id, partner_fnames)
