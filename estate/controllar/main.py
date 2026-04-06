from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError

class PropertyController(http.Controller):

    def _validate_inquiry_data(self, name, email):
        if not all([name, email]):
            raise ValidationError("Name and email are required fields")
        if '@' not in email or '.' not in email:
            raise ValidationError("Please enter a valid email address")

    @http.route(['/property/inquiry'], type='http', auth="public", website=True, methods=['GET', 'POST'], csrf=True)
    def property_inquiry(self, **post):
        if request.httprequest.method == 'GET':
            properties = request.env['estate.property'].sudo().search([('state', 'in', ['new', 'offer_received'])])
            return request.render('estate.property_inquiry_form', {
                'properties': properties,
                'submitted': post.get('submitted'), # Check if just submitted
            })

        try:
            name, email = post.get('name'), post.get('email')
            self._validate_inquiry_data(name, email)

            # CRM Lead Creation
            property_id = post.get('property_id')
            property_record = request.env['estate.property'].sudo().browse(int(property_id)) if property_id else None
            
            request.env['crm.lead'].sudo().create({
                'name': f'Property Inquiry - {property_record.name if property_record else "General"}',
                'partner_name': name,
                'email_from': email,
                'phone': post.get('phone'),
                'type': 'opportunity',
                'partner_id': request.env.user.partner_id.id if not request.env.user._is_public() else False,
                'description': f"Message: {post.get('message')}"
            })

            # Redirect back to the same page with a 'submitted' flag to show the message and clear fields
            return request.redirect('/property/inquiry?submitted=1')

        except Exception as e:
            # On error, we stay on the page but pass the error message
            properties = request.env['estate.property'].sudo().search([('state', 'in', ['new', 'offer_received'])])
            return request.render('estate.property_inquiry_form', {
                'properties': properties,
                'error_msg': str(e),
            })