from odoo import http
from odoo.http import request
from odoo.exceptions import UserError

class EstatePropertyOfferController(http.Controller):

    @http.route('/offer/<int:property_id>', auth='user', website=True)
    def make_an_offer(self, property_id):
        property = request.env['estate.property'].sudo().browse(property_id)

        if not property.exists():
            return request.render('website.404')

        return request.render('estate.estate_offer_form_page', {
            'property': property
        })

    @http.route('/submit-offer', auth='user', website=True, methods=['POST'], csrf=False)
    def submit_offer(self, **post):
        message = ''
        message_type = 'error'

        try:
            # Extract offer details from the POST request
            property_id = int(post.get('property_id'))
            price = float(post.get('price'))
            partner_id = request.env.user.partner_id.id
            validity = int(post.get('validity'))

            # Create the offer record
            request.env['estate.property.offer'].sudo().create({
                'property_id': property_id,
                'price': price,
                'partner_id': partner_id,
                'validity': validity,
            })

            message = 'Your offer has been submitted successfully.'
            message_type = 'success'

        except UserError as e:
            message = str(e)

        except Exception:
            message = 'An error occurred while processing your request. Please try again later.'

        property = request.env['estate.property'].sudo().search([('id', '=', property_id)])
        return request.render('estate.estate_property_detail_template', {
            'property': property,
            'message': message,
            'message_type': message_type
        })

