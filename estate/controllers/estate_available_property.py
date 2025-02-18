from odoo import http
from odoo.http import request

class EstateAvailableProperty(http.Controller):

    @http.route(['/estate/available_property', '/estate/available_property/page/<int:page>'], type='http', auth='public', methods=['GET'], website=True)
    def available_property(self, page=1, **kw):
        """
        Render a list of available properties with pagination.
        """
        Property = request.env['estate.property']

        domain = [('state', 'in', ['new', 'offer_received'])]
        listed_after = kw.get('listed_after')
        if listed_after:
            domain.append(('create_date', '>=', listed_after))

        property_count = Property.search_count(domain)
        url_args = {'listed_after': listed_after} if listed_after else {}

        pager = request.website.pager(
            url="/estate/available_property",
            total=property_count,
            page=page,
            step=6,
            url_args=url_args
        )

        properties = Property.search(domain, limit=6, offset=pager['offset'])

        return request.render('estate.available_property_listing', {
            'properties': properties,
            'page_name': 'properties',
            'default_url': '/estate/available_property',
            'pager': pager,
            'listed_after': listed_after or False,
        })


    @http.route('/estate/available_property_details/<int:id>', type='http', auth='public', website=True)
    def property_details(self, id, **kw):
        Property = request.env['estate.property']
        property = Property.browse(id)
        
        if not property:
            return request.not_found()

        return request.render('estate.available_property_details', {
            'property': property,
        })
