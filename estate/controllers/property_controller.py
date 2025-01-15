from odoo import http
from odoo.http import request

class PropertyController(http.Controller):
    
    @http.route('/properties', type='http', auth='public', website=True)
    def show_properties(self):
        """
        Renders the property listing page
        """
        # Fetch all properties (you can customize this query as per your requirements)
        properties = request.env['estate.property'].search([
            ('state', 'not in', ['sold', 'cancelled']),
            ('active', '=', True)
        ])     
        fetch_data = properties[:6]

        
        # Render the QWeb template and pass the properties to it
        return request.render('estate.property_listing_template', {
            'properties': fetch_data
        })
