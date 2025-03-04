from odoo import http
from odoo.http import request


class EstateAuctionController(http.Controller): 
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
     def list_properties(self, page=1, **kwargs):
        properties_per_page = 4
        page = int(page)
        # Apply filtering based on sell_type
        sell_type = kwargs.get("sell_type")
        domain = [('state', 'in', ('new', 'offer_received'))]
        if sell_type:
            domain.append(('sell_type', '=', sell_type))
        offset = (page - 1) * properties_per_page
        properties = request.env['estate.property'].sudo().search(domain, offset=offset, limit=properties_per_page)
        total_properties = request.env['estate.property'].sudo().search_count(domain)
        total_pages = (total_properties + properties_per_page - 1) // properties_per_page
        return request.render('estate.property_list', {
            'properties': properties,
            'current_page': page,
            'total_pages': total_pages,
            'selected_sell_type': sell_type,
        })
