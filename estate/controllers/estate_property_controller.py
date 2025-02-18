from odoo import http
from odoo.http import request

class RealEstateController(http.Controller):

    @http.route('/properties', auth='public', website=True)
    def list_properties(self, page=1, **kwargs):
        # Fetch properties that are available (not sold, not canceled)
        properties = request.env['estate.property'].search([
            ('state', 'in', ['new', 'available']),
            ('active', '=', True)
        ])
        
        # Pagination: limit to 6 properties per page
        properties = properties[(page-1)*6: page*6]
        
        # Calculate total pages for pagination
        total_pages = (len(properties) // 6) + (1 if len(properties) % 6 > 0 else 0)

        # Render the template and pass properties, page, and total_pages
        return request.render('estate.property_listing_template', {
            'properties': properties,
            'page': page,
            'total_pages': total_pages
        })
