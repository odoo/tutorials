from odoo import http
from odoo.http import request

class EstateAvailableProperty(http.Controller):

    @http.route('/estate/available_property', type='http', auth='public', methods=['GET'], website=True)
    def available_property(self, **kw):
        properties = request.env['estate.property'].search([
            ('state', 'in', ['new', 'offer_received'])
        ])

        return request.render('estate.available_property', {
            'properties': properties
        })
