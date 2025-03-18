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
        Properties = request.env['estate.property'].sudo().search([('is_published', '=', True)], limit=3)
        Agents = request.env['res.users'].sudo().search([], limit=4)
        return request.render('estate.property_listing_home_page', {
            'Properties': Properties,
            'Agents': Agents,
        })

    @http.route('/aboutus', type='http', auth='public', website=True, methods=['GET'])
    def render_about_us_page(self):
        return request.render('estate.property_listing_about_us_page', {})
