from odoo import http
from odoo.http import request

class PropertyController(http.Controller):

    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def property_list(self, page=1, listed_after=None, **kwargs):
        Property = request.env['estate.property'].sudo()
        domain = [('state', 'in', ('new', 'offer_received', 'offer_accepted'))]

        if listed_after:
            domain.append(('create_date','>=',listed_after))

        properties_per_page = 6
        properties = Property.search(domain, offset=(page-1)*properties_per_page, limit=properties_per_page)
        total_properties = Property.search_count(domain)

        return request.render('estate.estate_property_list_page', {
            'properties': properties,
            'pager': request.website.pager(
                url = '/properties',
                total = total_properties,
                page = page,
                step = properties_per_page
            )
        })

    @http.route('/property/<int:property_id>', type='http', auth='public', website=True)
    def property_detail(self, property_id):
        property = request.env['estate.property'].sudo().browse(property_id)

        return request.render('estate.estate_property_detail_page', {
            'property': property
        })
