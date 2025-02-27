from datetime import datetime
from odoo import http
from odoo.http import request


class EstatePropertyController(http.Controller):
    @http.route(['/properties', '/properties/page/<int:page>'], auth='public', website=True, type='http')
    def list_properties(self, page=1, **kwargs):
        domain = [('state', 'in', ['new', 'offer_accepted', 'offer_received'])]
        listed_date = kwargs.get('listed_date')
        min_price = kwargs.get('min_price')
        max_price = kwargs.get('max_price')

        if min_price:
            try:
                domain.append(('expected_price', '>=', float(min_price)))
            except ValueError:
                min_price = None

        if max_price:
            try:
                domain.append(('expected_price', '<=', float(max_price)))
            except ValueError:
                max_price = None

        if listed_date:
            try:
                listed_date = datetime.strptime(listed_date, '%Y-%m-%d').date()
                domain.append(('create_date', '>=', listed_date))
            except ValueError:
                listed_date = None

        url_args = kwargs
        properties_per_page = 6
        offset = (int(page) -1) * properties_per_page
        total_properties = request.env['estate.property'].sudo().search_count(domain)
        properties = request.env['estate.property'].sudo().search(
            domain,
            order='create_date desc',
            limit=properties_per_page,
            offset=offset
        )

        pager = request.website.pager(
            url = "/properties",
            total = total_properties,
            page = page,
            step = properties_per_page,
            scope = 3,
            url_args = url_args
        )
        return request.render('estate.estate_property_template', {
            'properties': properties,
            'pager': pager,
            'min_price': min_price,
            'max_price': max_price,
            'listed_date': listed_date,
        })

    @http.route('/property/<int:property_id>', auth='public', website=True, type='http')
    def property_details(self, property_id, **kwargs):
        property_obj = request.env['estate.property'].sudo().browse(property_id)
        if not property_obj.exists():
            return request.not_found()

        return request.render('estate.property_details_template', {
            'property': property_obj
        })
