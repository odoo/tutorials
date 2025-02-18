from odoo import http
from odoo.http import request, Response
import json

class Estate(http.Controller):
    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def property_list(self, page=1, **kwargs):
        Property = request.env['estate.property']  
        domain = [('state', 'in', ['new', 'offer_received'])]
        listed_after = kwargs.get('listed_after')
        if listed_after:
            domain.append(('create_date', '>=', listed_after))
        properties_count = Property.search_count(domain)
        pager = request.website.pager(
            url='/properties',
            total=properties_count,
            page=page,
            step=6,
            url_args={'listed_after': listed_after} if listed_after else {}
        )
        properties = Property.search(domain, limit=6, offset=pager['offset'])
        return request.render('estate.property_listing', {'properties': properties, 'pager': pager, 'listed_after': listed_after or False,})


    @http.route('/property/<int:id>', type='http', auth="public", website=True)
    def property_detail(self, id, **kwargs):
        property = request.env['estate.property'].sudo().browse(id)
        if not property:
            return request.not_found()
        return request.render('estate.property_detail', {
            'property': property,
        })
