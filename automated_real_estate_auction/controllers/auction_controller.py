from odoo import http
from odoo.http import request
from odoo.addons.estate.controllers.estate_property_controller import EstateController


class EstateAuctionController(EstateController): 
     @http.route('/auction/property/<int:property_id>', type="http", auth="public", website=True)
     def participate_in_property_auction(self, property_id):
        property = request.env['estate.property'].browse(property_id)
        if not property.exists():
            return request.redirect('/estate_property/properties')
        return request.render('automated_real_estate_auction.create_bid_template', {
            'property': property
        })

     @http.route("/property/auction/bid", type="http", auth="user", methods=["POST"], website=True)
     def create_bid(self, **post):
        property_id = int(post.get("property_id"))
        bid_amount = float(post.get("bid_amount"))
        # Get the property
        property = request.env['estate.property'].sudo().browse(property_id)
        if not property.exists():
            return request.redirect('/estate_property/properties')
        # Create the bid
        property.sudo().write({
            'offer_ids': [(0, 0, {
                'partner_id': request.env.user.partner_id.id,
                'price': bid_amount
            })],
            'state': 'offer_received',
            'best_price': max(property.best_price, bid_amount),  
            'highest_bidder': request.env.user.partner_id.id if bid_amount > property.best_price else property.highest_bidder.id
        })
        # Render a success page
        return request.render('automated_real_estate_auction.auction_success_template', {
            "message": "Congratulations! Your offer has been successfully placed. We will notify you the results as soon as the auction concludes.",
            "property": property
        })

     @http.route(['/estate_property/properties'], type='http', auth="public", website=True)
     def list_properties(self, page=1, domain=None, **kwargs):
        response = super().list_properties(page=page, **kwargs)
        sell_type = kwargs.get("sell_type")
        properties = response.qcontext.get('properties', request.env['estate.property'])
        if sell_type:
          properties = properties.filtered(lambda p: p.sell_type == sell_type)
        response.qcontext.update({'properties': properties})
        return response
