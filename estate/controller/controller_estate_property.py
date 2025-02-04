from odoo.http import Controller, request, route


class EstateWebsite(Controller):
    @route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def list_properties(self, page=1, **kwargs):
        step = 6
        offset = (page -1) * step

        price = kwargs.get('price')
        domain = [('state','in',['new', 'offer_received', 'offer_accepted'])]

        if price:
            domain.append(('expected_price', '<=', price))

        properties = (request.env['estate.property'].sudo().search(domain, limit=step, offset=offset))
        total_properties = (request.env['estate.property'].sudo().search_count(domain))
        
        pager = request.website.pager(
            url='/properties', total=total_properties, step=step, page=page, url_args=kwargs
        )

        return request.render(
            'estate.properties_list_page',
            {'properties': properties, 'pager': pager, 'price': price},
        )

    @route("/property/<model('estate.property'):property>", type='http', auth='public', website=True,
    )
    def property_details(self, property, **kwargs):
        return request.render('estate.property_detail_page', {'property': property})
