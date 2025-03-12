from odoo import http
from odoo.http import request
from odoo.addons.estate.controllers.estate_website import EstateWebsite

class EstateWebsite(EstateWebsite):
    
    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def list_properties(self, page=1, **kwargs):
        min_price = kwargs.get('min_price')
        max_price = kwargs.get('max_price')
        property_type = kwargs.get('property_type')
        sale_method = kwargs.get('sale_method')

        domain = ['|', ('status', '=', 'new'), ('status', '=', 'offer_received')]

        if min_price:
            domain.append(('expected_price', '>=', float(min_price)))
        if max_price:
            domain.append(('expected_price', '<=', float(max_price)))
        if property_type:
            domain.append(('property_type_id.name', '=', property_type))
        if sale_method:
            domain.append(('sale_method', '=', sale_method))
        
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

        return request.render('estate.listing_page', {
            'properties': properties,
            'pager': pager,
        })
        

   # Route to display the offer form for a specific property
    @http.route('/make-offer/<int:property_id>/', type='http', auth="user", website=True)
    def make_offer(self, property_id, **kwargs):
        property = request.env['estate.property'].sudo().browse(property_id)
        
        if not property.exists():
            return request.redirect('/properties')  # Redirect if property doesn't exist
        
        # Check if the current user has already made an offer on this property
        existing_offer = request.env['estate.property.offer'].sudo().search([
            ('property_id', '=', property.id),
            ('partner_id', '=', request.env.user.partner_id.id)
        ], limit=1)

        if existing_offer:
            return request.render('estate_auction_automation.website_view_offer_template', {
            'offer': existing_offer,
        })  # Redirect to view offer page
        
        return request.render('estate_auction_automation.website_make_offer_template', {
            'property': property,
            'user_name': request.env.user.name
        })

    # Route to view the offer details
    @http.route('/view-offer/<int:offer_id>/', type='http', auth="user", website=True)
    def view_offer(self, offer_id, **kwargs):
        offer = request.env['estate.property.offer'].sudo().browse(offer_ids)

        if not offer.exists():
            return request.redirect('/properties')  # Redirect if offer doesn't exist


    # Route to handle offer submission
    @http.route('/submit-offer', type='http', auth="user", website=True, csrf=False, methods=['POST'])
    def submit_offer(self, **post):
        try:
            user = request.env.user
            property_id = int(post.get('property_id'))
            offer_price = float(post.get('offer_price'))

            property = request.env['estate.property'].sudo().browse(property_id)
            if not property.exists():
                return request.redirect('/message?type=error&message=Property not found.')

            if not property.auction_deadline or property.state != '02_auction' or property.sale_method != 'auction':
                return request.redirect('/message?type=error&message=This property is not available for auction.')

            request.env['estate.property.offer'].sudo().create({
                'property_id': property_id,
                'partner_id': user.partner_id.id,
                'price': offer_price,
            })

      
            return request.redirect(
                f"/message?type=success&message=Your offer has been successfully placed."
                f"&offer_price={offer_price}&property_name={property.name}"
            )
        except Exception as e:
            request.env.cr.rollback()
            return request.redirect(f"/message?type=error&message={e}")

    # Route to display a generic message page
    @http.route('/message', type='http', auth="user", website=True)
    def message_page(self, **kwargs):
        return request.render('estate_auction_automation.website_generic_message_template', {
            'message_type': kwargs.get('type', 'error'),
            'message': kwargs.get('message', "Something went wrong. Please try again."),
            'offer_price': kwargs.get('offer_price'),
            'property_name': kwargs.get('property_name'),
        })
