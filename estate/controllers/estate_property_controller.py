from odoo import http
from odoo.http import request 

class EstatePropertyController(http.Controller):
    # Page that lists all properties
    @http.route('/properties', auth='public', type='http', website=True)
    def list_properties(self):
        properties = request.env['estate.property'].sudo().search([])
        return request.render('estate.property_list_template', {
            'properties': properties
        })

    # Page for viewing property details
    @http.route('/properties/<int:property_id>', auth='public', type='http', website=True)
    def property_details(self, property_id):
        estate_property = request.env['estate.property'].sudo().browse(property_id)
        if not estate_property.exists():
            return request.redirect('/properties')
        return request.render('estate.estate_property_details_template', {
            'property': estate_property
        })

    # Route to make an offer on a property
    @http.route('/properties/<int:property_id>/make_offer', type='http', auth='public', website=True, csrf=False)
    def make_offer(self, property_id, partner_id, offer_price, **kwargs):
        property_id = int(property_id)
        partner_id = int(partner_id)
        offer_price = float(offer_price)

        # Create the offer
        request.env['estate.property.offer'].sudo().create({
            'property_id': property_id,
            'partner_id': partner_id,
            'offer_price': offer_price,
        })
        return request.redirect(f'/properties/{property_id}')
