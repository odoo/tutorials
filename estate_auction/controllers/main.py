from odoo import http
from odoo.http import request

class AuctionPropertyController(http.Controller):
    
    @http.route("/property/auction/<model('estate.property'):property>", type="http", auth="user", website=True)
    def participate_in_auction(self, property, **kwargs):
        return request.render("estate_auction.create_bid", {"property": property})
    
    @http.route("/property/auction/bid", type="http", auth="user", website=True)
    def create_bid(self, **kwargs):
        property = request.env['estate.property'].search([('id', '=', kwargs['property_id'])])
        if(property.best_price < float(kwargs['bid_amount'])):
            property.sudo().write({
                'offer_ids': [(0, 0, {
                    'partner_id': request.env.user.partner_id.id,
                    'price': float(kwargs['bid_amount'])
                })],
                'best_price': float(kwargs['bid_amount']),
                'state': 'offer_received',
                'highest_bidder': request.env.user.partner_id.id
            })
        else:
            property.sudo().write({
                'offer_ids': [(0, 0, {
                    'partner_id': request.env.user.partner_id.id,
                    'price': float(kwargs['bid_amount'])
                })],
                'state': 'offer_received',
            })
        return request.render('estate_auction.generic_message', {"message": "Congratulations! Your offer has been successfully placed we will notify you of the results as soon as the auction concludes"})
