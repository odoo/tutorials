from odoo import http
from odoo.http import request

class EstatePropertyController(http.Controller):

    @http.route('/properties', auth='public', website=True)
    def list_properties(self, availability='available', property_type='all'):

        search_filters = {
            'all': [],
            'available': ['new', 'offer_received']
        }

        property_types = request.env['estate.property.type'].sudo().search([])

        domain = []
        if availability == "available":
            domain.append(('state', 'in', search_filters[availability]))
        if property_type != 'all':
            domain.append(('property_type_id', '=', int(property_type)))

        properties = request.env['estate.property'].sudo().search(domain)

        return request.render('estate.estate_property_listing_template', {
            'properties': properties,
            'property_types': property_types,
            'selected_availability': availability,
            'selected_property_type': property_type
        })

    @http.route('/properties/<int:property_id>', auth='public', website=True)
    def property_details(self, property_id):
        property = request.env['estate.property'].sudo().search([('id', '=', property_id)])
        return request.render('estate.estate_property_detail_template', {
            'property': property,
        })
