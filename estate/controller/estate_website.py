from odoo import http
from odoo.http import request

class EstateWebsite(http.Controller):

    @http.route(['/properties'], type='http', auth="public", website=True, methods=['GET'])
    def list_properties(self):
        """Displays a list of available properties that are published and not sold."""
        properties = request.env['estate.property'].sudo().search(
            [('is_published', '=', True), ('state', '!=', 'sold')],
            order='name asc'
        )
        return request.render('estate.property_listing_template', {'properties': properties})

    @http.route('/property/details/<int:property_id>', type='http', auth='public', website=True, methods=['GET'])
    def property_details(self, property_id):
        """Displays detailed information about a specific property."""
        property_obj = request.env['estate.property'].sudo().browse(property_id)
        if not property_obj.exists():
            return request.not_found()
        return request.render('estate.property_detail_template', {'property': property_obj})

    @http.route('/', type='http', auth='public', website=True, methods=['GET'])
    def render_homepage(self):
        """Renders the homepage."""
        return request.render('estate.property_listing_home_page', {})

    @http.route('/aboutus', type='http', auth='public', website=True, methods=['GET'])
    def render_about_us_page(self):
        """Renders the About Us page."""
        return request.render('estate.property_listing_about_us_page', {})
