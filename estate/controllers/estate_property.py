from datetime import datetime
from odoo import http
from odoo.http import request


class EstatePropertyController(http.Controller):
    @http.route(['/properties', '/properties/page/<int:page>'], auth='public', website=True, type='http')
    def list_properties(self, page=1, listed_date=None, **kwargs):
        domain = [('state', 'in', ['new', 'offer_accepted', 'offer_received'])]
        url_args = dict()

        if listed_date:
            listed_date = datetime.strptime(listed_date, '%Y-%m-%d').date()
            domain += [('create_date', '>=', listed_date)]
            url_args['listed_date'] = listed_date

        offset = (int(page) -1) * 6
        total_properties = request.env['estate.property'].sudo().search_count(domain)
        properties = request.env['estate.property'].sudo().search(domain, order='create_date desc', limit=6, offset=offset)

        pager = request.website.pager(
            url = "/properties",
            total = total_properties,
            page = page,
            step = 6,
            scope = 3,
            url_args = url_args
        )
        return request.render('estate.estate_property_template', {
            'properties': properties,
            'pager': pager,
        })

    @http.route('/property/<int:property_id>', auth='public', website=True, type='http')
    def property_details(self, property_id, **kwargs):
        property_obj = request.env['estate.property'].sudo().browse(property_id)
        if not property_obj.exists():
            return request.not_found()

        return request.render('estate.property_details_template', {
            'property': property_obj
        })
