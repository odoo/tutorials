from odoo import http
from odoo.http import request

from odoo.addons.estate.controllers.estate_property import EstatePropertyController

class EstatePropertyController(EstatePropertyController):
    
    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def list_properties(self, page=1, **kwargs):
        response = super().list_properties(page, **kwargs)

        domain = response.qcontext.get('domain', [])
        
        if 'property_sell_type' in kwargs:
            domain.append(('property_sell_type', '=', kwargs['property_sell_type']))

        properties = request.env['estate.property'].sudo().search(
            domain, limit=3, offset=(page - 1) * 3
        )

        response.qcontext.update({
            'properties': properties,
        })

        return response

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
                return request.redirect('/message?type=error&message=Invalid property or offer price.')

            property_id = int(property_id)
            offer_price = float(offer_price)

            # Ensure the property exists
            property = request.env['estate.property'].sudo().browse(property_id)
            if not property.exists():
                return request.redirect('/message?type=error&message=Property not found.')

            if not property.auction_end_time or property.state != '02_auction' or property.property_sell_type != 'auction':
                return request.redirect('/message?type=error&message=This property is not available for auction.')

            request.env['estate.property.offer'].sudo().create({
                'property_id': property_id,
                'partner_id': user.partner_id.id,
                'price': offer_price,
            })

            return request.redirect('''/message?
                type=success&
                message=Your offer has been successfully placed.
                    We will notify you of the results as soon as the auction concludes.''')

        except Exception as e:
            request.env.cr.rollback()
            return request.redirect(f'/message?type=error&message={e}')

    @http.route('/message', type='http', auth="user", website=True)
    def message_page(self, **kwargs):
        """ A generic message page for success and error messages """
        message_type = kwargs.get('type', 'error')
        message = kwargs.get('message', "Something went wrong. Please try again.")
        return request.render('estate_auction_automation.website_generic_message_template', {
            'message_type': message_type,
            'message': message
        })
