from odoo import http
from odoo.http import request

class EstateWebsiteController(http.Controller):

    @http.route('/properties', type='http', auth='public', website=True)
    def list_properties(self, min_price=0, max_price=0, **kwargs):
        domain = []
        try:
            min_price = float(min_price)
        except (ValueError, TypeError):
            min_price = 0
        try:
            max_price = float(max_price)
        except (ValueError, TypeError):
            max_price = 0

        if min_price:
            domain.append(('selling_price', '>=', min_price))
        if max_price:
            domain.append(('selling_price', '<=', max_price))

        properties = request.env['estate.property'].sudo().search(domain)

        return request.render('estate.property_listing', {
            'properties': properties,
            'min_price': min_price,
            'max_price': max_price,
        })

    @http.route('/properties/<int:property_id>', type='http', auth='public', website=True)
    def property_detail(self, property_id, **kwargs):
        property_rec = request.env['estate.property'].sudo().browse(property_id)
        if not property_rec.exists():
            return request.not_found()

        return request.render('estate.property_detail', {
            'property': property_rec
        })
