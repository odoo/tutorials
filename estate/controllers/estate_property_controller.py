from odoo import http
from odoo.http import request


class EstatePropertyController(http.Controller):

    @http.route(['/estate/properties', '/estate/properties/page/<int:page>'], auth='public', website=True)
    def my_website(self, page=1, **kwargs):
        Property = request.env['estate.property'].sudo()
        
        # Pagination variables
        properties_per_page = 6
        total_properties = Property.search_count([('state', 'not in', ['sold', 'cancelled'])])
        total_pages = (total_properties // properties_per_page) + (1 if total_properties % properties_per_page > 0 else 0)

        # Fetch only required records using `offset` and `limit`
        properties = Property.search(
            [('state', 'not in', ['sold', 'cancelled'])], 
            offset=(page - 1) * properties_per_page, 
            limit=properties_per_page
        )

        return request.render('estate.property_list_template', {
            'properties': properties,
            'page': page,
            'total_pages': total_pages
        })

    @http.route('/estate/properties/<int:property_id>', type='http', auth="public", website=True)
    def property_details(self, property_id, **kwargs):
        property_obj = request.env['estate.property'].sudo().browse(property_id)
        if not property_obj.exists():
            return request.render('website.404')

        return request.render('estate.property_detail_template', {
            'property': property_obj
        })
