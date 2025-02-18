from odoo import http, _
from odoo.http import request


class EstatePropertyController(http.Controller):

    @http.route('/properties', type='http', auth='public', website = True)
    def list_properties(self, **kwargs):
        domain = [('state','in',["new","offer_accepted","offer_received"])]
        properties = request.env['estate.property'].sudo().search(domain)
        return request.render('estate.list_properties_template',{ 'properties': properties})

    @http.route('/properties/<int:property_id>', type='http', auth='public', website = True)
    def show_property_details(self, property_id):
        property = request.env['estate.property'].sudo().browse((property_id,))
        return request.render('estate.property_detail_template',{'property':property})
