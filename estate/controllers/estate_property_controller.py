from odoo import http
from odoo.http import request
from datetime import datetime


class EstatePropertyController(http.Controller):
    @http.route('/estate_properties', auth='public', type='http', website=True)
    def estate_property_list(self, **kwargs):
        page = max(1, int(kwargs.get('page', 1)))
        filter_date = kwargs.get('filter_date', None)

        domain = [('state', 'in', ['new', 'offer_received', 'offer_accepted'])]
        if not request.env.user.has_group("estate.estate_group_manager"):
            domain.append(('published', '=', True))
        if filter_date:
            domain.append(('create_date', '>=', filter_date))

        properties = request.env['estate.property'].sudo().search(domain, order='create_date desc', offset=(int(page) - 1) * 9, limit=9)
        has_next = len(request.env['estate.property'].sudo().search(domain, offset=int(page) * 9, limit=1)) > 0

        return request.render('estate.property_list_template', {
                'properties': properties, 
                'page': int(page),
                'has_next': has_next,
                'filter_date': filter_date
            })

    @http.route(['/property/<int:property_id>'], auth='public', type='http', website=True)
    def estate_property_details(self, property_id, **kwargs):
        property = request.env['estate.property'].sudo().browse(property_id)
        if not property.exists():
            return request.not_found()

        return request.render('estate.website_property_details', {
            'property': property,
            'offers': property.property_offer_ids
        })
