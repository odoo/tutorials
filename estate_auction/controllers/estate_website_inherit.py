from odoo import http
from odoo.http import request, Controller, route
from odoo.addons.estate.controllers.main import EstatePropertyController


class EstatePropertyControllerInherit(EstatePropertyController):

    @route(['/properties', '/properties/page/<int:page>'], type='http', auth="public", website=True)
    def list_properties(self, page=1, **kwargs):
        response = super().list_properties(page, **kwargs)

        selected_auction_type = kwargs.get('auction_type')
        if selected_auction_type:
            properties = response.qcontext.get('properties', request.env['estate.property'])
            filtered_properties = properties.filtered(lambda p: p.auction_type == selected_auction_type)

            response.qcontext.update({
                'properties': filtered_properties,
                'selected_auction_type': selected_auction_type
            })
        return response

    @http.route(['/properties/<int:property_id>/offer'], type='http', auth="user", website=True)
    def create_offer_form(self, property_id):
        property_details = request.env['estate.property'].sudo().browse(property_id)
        user = request.env.user.partner_id
        return request.render('estate_auction.create_offer_template', {
            'property_details': property_details,
            'partner_name': user.name
        })
    
    @http.route(['/properties/<int:property_id>/offer/submit'], type='http', auth="user", website=True, methods=['POST'])
    def submit_offer(self, property_id, **post):
        request.env['estate.property.offer'].sudo().create({
            'partner_id': request.env.user.partner_id.id,
            'property_id': property_id,
            'price': float(post.get('amount', 0))
        })
        return request.redirect('/properties/{}/offer/success'.format(property_id))
    
    @http.route(['/properties/<int:property_id>/offer/success'], type='http', auth="user", website=True)
    def offer_success(self, property_id):
        return request.render('estate_auction.offer_success_template', {})
