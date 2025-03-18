from odoo import http
from odoo.http import request

class PropertyLsitController(http.Controller):
    @http.route('/property', auth='public', type='http', website=True)
    def get_property_list(self):
        properties = request.env['real.estate.property'].search([])

        properties_list = []
        for property in properties:
            properties_list.append({
                'id': property.id,
                'name': property.name,
                'image': property.image,
                'description': property.description,
                'postcode': property.postcode,
                'date_availability': property.date_availability,
                'expected_price': property.expected_price,
                'bedrooms': property.bedrooms,
                'living_area': property.living_area,
                'facades': property.facades,
                'garage': property.garage,
                'garden':property.garden,
                'garden_area': property.garden_area,
                'garden_orientation': property.garden_orientation,
                'status': property.status,
                'type': property.property_type_id.name if property.property_type_id else '',
            })

        return request.render('real_estate.property_list_template', {'properties': properties_list})

    @http.route('/property/<int:property_id>', auth='public', type='http', website=True)
    def view_property(self, property_id):
        # Fetch the specific property by ID
        property = request.env['real.estate.property'].browse(property_id)

        if property.exists():
            property_data = {
                 'id': property.id,
                'name': property.name,
                'image': property.image,
                'description': property.description,
                'postcode': property.postcode,
                'date_availability': property.date_availability,
                'expected_price': property.expected_price,
                'bedrooms': property.bedrooms,
                'living_area': property.living_area,
                'facades': property.facades,
                'garage': property.garage,
                'garden':property.garden,
                'garden_area': property.garden_area,
                'garden_orientation': property.garden_orientation,
                'status': property.status,
                'type': property.property_type_id.name if property.property_type_id else '',
            }

            return request.render('real_estate.property_view_template', {'property': property_data})

        else:
            return request.not_found()