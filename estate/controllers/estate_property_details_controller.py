from odoo import http
from odoo.http import request

class EstateProertyDetailsController(http.Controller):
        @http.route('/property/<int:property_id>', type='http', auth='public', website=True)
        def property_details(self, property_id, **kwargs):
            property_obj = request.env['estate.property'].browse(property_id)

            if not property_obj.exists():
                return request.render('website.404')  # Show 404 if not found

            return request.render('estate.property_detail_template', {
                'property': property_obj
            })
            