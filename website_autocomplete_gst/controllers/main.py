from odoo.http import request, route

from odoo.addons.website_sale.controllers import main


class WebsiteSale(main.WebsiteSale):
    @route('/shop/get_data', type='json', auth='public', website=True, sitemap=False)
    def get_company_details(self):
        vat = request.params.get('vat')
        if not vat:
            return {"error": "VAT number is missing"}
        partner = request.env['res.partner']._get_company_details_from_vat(vat)
        return partner if partner else {}
