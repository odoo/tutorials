from odoo import http
from odoo.http import request


class RealEstateWebsite(http.Controller):
    
    @http.route('/properties', type='http', auth='public', website=True)
    def property_list(self, **kwargs):
        properties = request.env['estate.property'].sudo().search([])
        message = kwargs.get('message', '')
        return request.render('real_estate.property_listing', {'properties':properties, 'message': message})

    @http.route('/properties/<int:property_id>', type='http', auth="public", website=True)
    def property_view(self, property_id, **kwargs):
        property = request.env['estate.property'].sudo().browse(property_id)
        if not property.exists():
            return request.render.not_found()
        return request.render('real_estate.property_detail', {'property': property})

    @http.route('/properties/inquire', type='http', auth="public", website=True, methods=['POST'], csrf=True)
    def property_inquire(self, **post):
        property_id = int(post.get('property_id', 0))
        property_obj = request.env['estate.property'].sudo().browse(property_id)

        if not property_obj.exists():
            return request.not_found()

        request.env['estate.inquiry'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'message': post.get('message'),
            'property_id': property_id
        })

        # message_body = f"""
        # New Inquiry:
        # Name: {post.get('name')}
        # Email: {post.get('email')}
        # Phone: {post.get('phone')}
        # Message: {post.get('message')}
        # """

        # property_obj.message_post(body=message_body, subject="New Property Inquiry")

        return request.redirect('/properties?message=success')
