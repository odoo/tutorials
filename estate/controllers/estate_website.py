from odoo import http
from odoo.http import request


class EstateWebsite(http.Controller):
    @http.route(['/properties', '/properties/page/<int:page>'], type='http',
        auth='public', website=True,
    )
    def list_properties(self, page=1, **kwargs):
        step = 6
        offset = (page - 1) * step

        domain = [('state', 'in', ['new', 'offer_received', 'offer_accepted']), ('active', '=', True)]

        # Search by Property Name
        search_query = kwargs.get('search')
        if search_query:
            domain.append(('name', 'ilike', search_query))

        # Filter by Price Range
        min_price = kwargs.get('min_price')
        max_price = kwargs.get('max_price')
        if min_price:
            domain.append(('expected_price', '>=', float(min_price)))
        if max_price:
            domain.append(('expected_price', '<=', float(max_price)))

        # Sorting Options
        sort_by = kwargs.get('sort_by', 'create_date desc')
        if sort_by not in ['create_date desc', 'expected_price asc', 'expected_price desc']:
            sort_by = 'create_date desc'

        # Fetch filtered and sorted properties
        properties = request.env['estate.property'].sudo().search(domain, limit=step, offset=offset, order=sort_by)

        total_properties = request.env['estate.property'].sudo().search_count(domain)

        pager = request.website.pager(
            url='/properties', total=total_properties, step=step, page=page, url_args=kwargs
        )

        return request.render(
            'estate.properties_list_page',
            {
                'properties': properties,
                'pager': pager,
                'search_query': search_query,
                'min_price': min_price,
                'max_price': max_price,
                'sort_by': sort_by
            },
        )

    @http.route("/property/<model('estate.property'):property>", type='http',
        auth='public', website=True,
    )
    def property_details(self, property, **kwargs):
        return request.render('estate.property_detail_page', {'property': property})
