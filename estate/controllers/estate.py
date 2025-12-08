from odoo.http import Controller, request, route


class EstateController(Controller):
    @route(['/properties', '/properties/page/<int:page>'], auth='public', website=True)
    def fetch_properties(self, page=1, **kwargs):
        search_domains = [('state', 'in', ['new', 'offer_received'])]
        query_params = {}

        min_price_str = kwargs.get('min_price')
        max_price_str = kwargs.get('max_price')
        date_str = kwargs.get('date')

        if date_str:
            search_domains.append(('create_date', '>=', date_str))
            query_params['date'] = date_str

        if min_price_str:
            try:
                float(min_price_str)
                search_domains.append(('expected_price', '>=', min_price_str))
                query_params['min_price'] = min_price_str
            except ValueError:
                pass

        if max_price_str:
            try:
                float(max_price_str)
                search_domains.append(('expected_price', '<=', max_price_str))
                query_params['max_price'] = max_price_str
            except ValueError:
                pass

        properties = (
            request.env['estate.property']
            .sudo()
            .search(search_domains, order='create_date desc')
        )

        items_per_page = 10
        total_items = len(properties)
        start_index = items_per_page * (page - 1)
        page_items = properties[start_index : start_index + items_per_page]

        pager = request.website.pager(
            url='/properties',
            total=total_items,
            page=page,
            step=items_per_page,
            url_args=query_params,
        )

        return request.render(
            'estate.property_template',
            {
                'properties': page_items,
                'pager': pager,
                'date': date_str,
                'min_price': min_price_str,
                'max_price': max_price_str,
            },
        )

    @route('/property/<int:property_id>', auth='public', website=True)
    def property_detail(self, property_id):
        estate = request.env['estate.property'].sudo().browse(property_id)
        if not estate.exists():
            return request.not_found()

        return request.render('estate.property_details_template', {'property': estate})
