from odoo import http
from odoo.http import request

class AuctionPropertyController(http.Controller):
    @http.route("/property/auction/<model('estate.property'):property>", type="http", auth="user", website=True)
    def participate_in_auction(self, property, **kwargs):
        try:
            property_bids = request.env['estate.property.offer'].sudo().search([
                ('property_id', '=', property.id),
                ('partner_id', '=', request.env.user.partner_id.id)
            ])
            if property_bids:
                return request.render('estate_auction.generic_message', {"title":"Oops!", "message": "You can only place one bid on a property"})
            return request.render("estate_auction.create_bid", {"property": property})
        except Exception as e:
            return request.render('estate_auction.generic_error', {"error": e, "id": property.id})
    
    @http.route("/property/auction/bid", type="http", auth="user", website=True)
    def create_bid(self, **kwargs):
        try:
            property = request.env['estate.property'].search([('id', '=', kwargs['property_id'])])
            property.sudo().write({
                'offer_ids': [(0, 0, {
                    'partner_id': request.env.user.partner_id.id,
                    'price': float(kwargs['bid_amount'])
                })],
                'state': 'offer_received',
            })
            return request.render('estate_auction.generic_message', {"title":"Congratulations!", "message": "Congratulations! Your offer has been successfully placed we will notify you of the results as soon as the auction concludes"})
        except Exception as e:
            return request.render('estate_auction.generic_error', {"error": e, "expected_price":property.expected_price, "id": property.id})
            