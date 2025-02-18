from odoo import http
from odoo.http import request

class EstatePropertyController(http.Controller):

    @http.route(['/properties', '/properties/page/<int:page>'], auth='public', website=True)
    def list_properties(self, page=1, **kwargs):
        domain = [('state', 'in', ['new', 'offer_received'])]

        # Handle date filter
        listed_after = kwargs.get('listed_after')
        if listed_after:
            domain.append(('create_date', '>=', listed_after))

        # Pagination setup
        properties_per_page = 6
        offset = (page - 1) * properties_per_page

        # Fetch filtered properties
        properties = request.env['estate.property'].sudo().search(
            domain, order='create_date desc', offset=offset, limit=properties_per_page)

        total_properties = request.env['estate.property'].sudo().search_count([
            ('state', 'not in', ['sold', 'cancelled'])
        ])

        pager = request.website.pager(
            url='/properties',
            total=total_properties,
            page=page,
            step=properties_per_page,
        )

        return request.render('estate.estate_property_template', {
            'properties': properties,
            'pager': pager,
            'listed_after': listed_after,
        })

    @http.route('/property/<int:property_id>', auth='public', website=True)
    def property_detail(self, property_id, **kwargs):
        property_obj = request.env['estate.property'].sudo().browse(property_id)
        if not property_obj.exists():
            return request.not_found()

        return request.render('estate.estate_property_detail_template', {
            'property': property_obj
        })
