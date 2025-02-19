from odoo import http
from odoo.http import request

class EstateController(http.Controller):

    @http.route('/properties', type='http', auth="public", website=True)
    def property_listing(self, page=1, **kwargs):
        Property = request.env['estate.property'].sudo()
        per_page = 6
        total_properties = Property.search_count([])  
        total_pages = (total_properties // per_page) + (1 if total_properties % per_page > 0 else 0)
        page = int(page)
        properties = Property.search([], offset=(page - 1) * per_page, limit=per_page)

        return request.render('estate.property_listing', {
            'properties': properties,
            'total_pages': total_pages,
            'current_page': int(page),
        })

    @http.route('/properties/<int:property_id>', type='http', auth="public", website=True)
    def property_details(self, property_id, **kwargs):
        """Redirect to the backend view of the selected property."""
        property_record = request.env['estate.property'].sudo().browse(property_id)
        if not property_record.exists():
            return request.not_found()
        
        return request.render('estate.property_detail', {'property': property_record})
