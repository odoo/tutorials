from odoo import http
from odoo.http import request


class PropertyController(http.Controller):

    @http.route('/properties', type='http', auth='public', website=True)
    def list_properties(self, **kwargs):
        properties = request.env['estate.property'].sudo().search([('state', 'in', ['new', 'offer_recieved'])])
        return request.render('estate.property_page', {
            'properties': properties
        })

    @http.route('/property/<model("estate.property"):prop>', type='http', auth='public', website=True)
    def property_detail(self, prop):
        return request.render('estate.property_detail_page', {
            'property': prop
        })
