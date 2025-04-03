from datetime import datetime
from odoo import http
from odoo.http import request

class OfferController(http.Controller):
    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth="public", website=True, csrf=False, methods=['GET', 'POST'])
    def list_properties(self, page=1, **kwargs):
        properties_per_page = 6
        domain = []

        if request.httprequest.method == 'POST':
            bid_type = request.params.get('bid_type')
            search_query = request.params.get('search', '').strip()
            property_status = request.params.get('property_status')
            min_price = request.params.get('min_price')
            max_price = request.params.get('max_price')
        else:
            bid_type = kwargs.get('bid_type')
            search_query = kwargs.get('search', '').strip()
            property_status = kwargs.get('property_status')
            min_price = kwargs.get('min_price')
            max_price = kwargs.get('max_price')

        if search_query:
            domain += ['|', ('name', 'ilike', search_query), ('description', 'ilike', search_query)]

        if bid_type:
            domain.append(('bid_type', '=', bid_type))

        if property_status:
            domain.append(('status', '=', property_status))

        if min_price:
            domain.append(('expected_price', '>=', float(min_price)))
        if max_price:
            domain.append(('expected_price', '<=', float(max_price)))
        
        properties = request.env['estate.property'].sudo().search(domain)
        now = datetime.now()
        for property in properties:
            if property.bid_type == 'auction' and property.auction_end_time and property.auction_end_time <= now:
                property.sudo().write({'auction_status': 'auction_ended'})  # Update auction status

        total_properties = request.env['estate.property'].sudo().search_count(domain)
        pager = request.website.pager(
            url='/properties',
            total=total_properties,
            page=page,
            step=properties_per_page,
            url_args={'search': search_query, 'bid_type': bid_type, 'property_status': property_status, 'min_price': min_price, 'max_price': max_price} if any([search_query, bid_type, property_status, min_price, max_price]) else {}
        )

        properties = request.env['estate.property'].sudo().search(
            domain,
            offset=pager['offset'],
            limit=properties_per_page
        )

        return request.render('real_estate.website_property_template', {
            'properties': properties,
            'pager': pager,
            'search_query': search_query,
            'bid_type': bid_type,
            'property_status': property_status,
            'min_price': min_price,
            'max_price': max_price
        })

    @http.route('/property/<int:property_id>', type='http', auth="public", website=True)
    def property_details(self, property_id):
        property_obj = request.env['estate.property'].sudo().browse(property_id)
        if not property_obj.exists():
            return request.not_found()

        return request.render('real_estate.website_property_template', {
            'property': property_obj,
            'auction_end_time': property_obj.auction_end_time,  # Pass to template
        })

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

        request.env['estate.property.offer'].sudo().create({
            'property_id': property_id,
            'partner_id': request.env.user.partner_id.id,
            'price': offer_amount,
        })
        return request.redirect('/congratulations')

    @http.route('/congratulations', type='http', auth="public", website=True)
    def congratulations_page(self):
        return request.render('estate_auction.congratulations_template')
