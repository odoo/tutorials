from odoo import http
from odoo.http import request


class EstateProperties(http.Controller):
    @http.route("/properties", website=True, auth="public")
    def get_properties(self, page=1, **kwargs):
        properties = request.env['estate.property'].sudo().search([('state', 'not in', ['sold', 'cancelled'])], limit=6, offset=(int(page) - 1)*6)
        total_properties = request.env['estate.property'].sudo().search_count([('state', 'not in', ['sold', 'cancelled'])])
        
        # Calculate total pages
        total_pages = (total_properties / 6) 
        
        # Render the property listing page
        return request.render('estate.estate_property_listing_template', {
            'properties': properties,
            'total_pages': total_pages,
            'current_page': page,
        })
