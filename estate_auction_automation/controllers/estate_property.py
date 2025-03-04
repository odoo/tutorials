from odoo import http
from odoo.http import request

from odoo.addons.estate.controllers.estate_property import EstatePropertyController

class EstatePropertyController(EstatePropertyController):
    
    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def list_properties(self, page=1, **kwargs):
        min_price = kwargs.get('min_price')
        max_price = kwargs.get('max_price')
        property_type = kwargs.get('property_type')
        property_sell_type = kwargs.get('property_sell_type')

        domain = ['|', ('stage', '=', 'new'), ('stage', '=', 'offer_received')]

        if min_price:
            domain.append(('expected_price', '>=', float(min_price)))
        if max_price:
            domain.append(('expected_price', '<=', float(max_price)))
        if property_type:
            domain.append(('property_type_id.name', '=', property_type))
        if property_sell_type:
            domain.append(('property_sell_type', '=', property_sell_type))
        
        properties_per_page = 3
        total_properties = request.env['estate.property'].sudo().search_count(domain)
        
        properties = request.env['estate.property'].sudo().search(
            domain, limit=properties_per_page, offset=(page - 1) * properties_per_page
        )

        filter_query = {key: val or '' for key, val in kwargs.items()}
        pager = request.website.pager(
            url='/properties',
            url_args=filter_query,
            total=total_properties,
            page=page,
            step=properties_per_page
        )

        return request.render('estate.website_property_listing_template', {
            'properties': properties,
            'pager': pager,
        })

    @http.route('/make-offer/<int:property_id>', type='http', auth="user", website=True)
    def make_offer(self, property_id, **kwargs):
        property = request.env['estate.property'].sudo().browse(property_id)
        user_name = request.env.user.name

        return request.render('estate_auction_automation.website_make_offer_template', {
            'property': property,
            'user_name': user_name
        })

    @http.route('/submit-offer', type='http', auth="user", website=True, csrf=False, methods=['POST'])
    def submit_offer(self, **post):
        """ Handle offer form submission and create an offer record """
        try:
            # Validate input values
            user = request.env.user
            property_id = post.get('property_id')
            offer_price = post.get('offer_price')

            if not property_id or not offer_price:
                return request.redirect('/not-found')

            property_id = int(property_id)
            offer_price = float(offer_price)

            # Ensure the property exists
            property = request.env['estate.property'].sudo().browse(property_id)
            if not property.exists():
                return request.redirect('/not-found')

            if not property.auction_end_time or property.state != '02_auction' or property.property_sell_type != 'auction':
                return request.redirect('/not-found')  # Redirect if conditions are not met

            request.env['estate.property.offer'].sudo().create({
                'property_id': property_id,
                'partner_id': user.partner_id.id,  # Corrected: use `partner_id`
                'price': offer_price,
            })

            return request.redirect('/thank-you')

        except Exception as e:
            request.env.cr.rollback()
            return request.redirect('/error-page')

    @http.route('/thank-you', type='http', auth="user", website=True)
    def thank_you(self):
        return request.render("estate_auction_automation.website_thank_you_template")
    
    @http.route('/not-found', type='http', auth="user", website=True)
    def not_found(self):
        return request.render("estate_auction_automation.website_not_found_template")
