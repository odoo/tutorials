from odoo import http
from odoo.http import request


class EstateController(http.Controller):
    @http.route(['/estate_property/properties'], type='http', auth='public', website=True)
    def list_properties(self, page=1, domain=None, **kwargs):
        properties_per_page = 4
        page = int(page)
        offset = (page - 1) * properties_per_page
        domain = [('state', 'in', ('new', 'offer_received'))]
        properties = request.env['estate.property'].search(domain, offset=offset, limit=properties_per_page)
        total_properties = request.env['estate.property'].search_count(domain)
        total_pages = (total_properties + properties_per_page - 1) // properties_per_page
        return request.render('estate.property_list', {
            'properties': properties,
            'current_page': page,
            'total_pages': total_pages
        })

    @http.route('/property/<int:property_id>', type='http', auth='public', website=True)
    def property_detail(self, property_id):
        property = request.env['estate.property'].browse(property_id)
        if not property.exists():
            return request.redirect('/estate_property/properties')
        return request.render('estate.property_detail', {
            'property': property
        })    

    @http.route(['/property/search'], type='http', auth='public', website=True)
    def search_properties(self, property_type=None, **kwargs):
        page = kwargs.get('page', 1)
        properties_per_page = 4
        page = int(page)
        domain = ['|', ('state', '=', 'new'), ('state', '=', 'offer_accepted')]  # Default filter for properties
        if property_type:
            domain.append(('property_type_id', '=', int(property_type)))  # Filter by selected property type
        offset = (page - 1) * properties_per_page # Number of properties we have to skip to get properties for current page 
        properties = request.env['estate.property'].search(domain, offset=offset, limit=properties_per_page)
        total_properties = request.env['estate.property'].search_count(domain)
        total_pages = (total_properties + properties_per_page - 1) // properties_per_page
        # Get the available property types to display in the search dropdown
        property_types = request.env['estate.property.type'].search([])
        # Render the template with filtered properties and property types
        return request.render('estate.filter_properties', {
            'properties': properties,
            'property_types': property_types,
            'current_page': page,
            'total_pages': total_pages
        })
