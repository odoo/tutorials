from odoo import http
from odoo.http import request

class OfferController(http.Controller):

    @http.route('/create/offer/<int:property_id>', type='http', auth="user", website=True)
    def create_offer_form(self, property_id, **kwargs):
        property_obj = request.env['estate.property'].sudo().browse(property_id)

        if not property_obj.exists():
            return request.not_found()

        user = request.env.user 

        return request.render('estate_auction.create_offer_form_template', {
            'property': property_obj,
            'user': user,
        })

    @http.route('/submit/offer', type='http', auth="user", methods=['POST'], website=True, csrf=False)
    def submit_offer(self, **post):
        property_id = int(post.get('property_id'))
        offer_amount = float(post.get('offer_amount'))

        # if offer_amount <= expected_price:
        #     return request.redirect(f'/create/offer/{property_id}') 
        
        # request.env['real.estate.offer'].sudo().create({
        #     'property_id': property_id,
        #     'partner_id': request.env.user.partner_id.id,
        #     'price': offer_amount,
        # })

        request.env['estate.property.offer'].sudo().create({
            'property_id': property_id,
            'partner_id': request.env.user.partner_id.id,
            'price': offer_amount,
        })

        return request.redirect('/congratulations')

    @http.route('/congratulations', type='http', auth="public", website=True)
    def congratulations_page(self):
        return request.render('estate_auction.congratulations_template')
