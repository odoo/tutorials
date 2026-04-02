from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class PropertyController(http.Controller):
    def _validate_inquiry_data(self, name, email):
        """Validate inquiry data and raise ValidationError if invalid."""
        if not all([name, email]):
            raise ValidationError("Name and email are required fields")

        if '@' not in email or '.' not in email:
            raise ValidationError("Please enter a valid email address")

    @http.route(['/properties'], type='http', auth="public", website=True)
    def property_list(self, **post):
        properties = request.env['estate.property'].sudo().search([])
        return request.render('estate.property_list_template', {
            'properties': properties,
        })

    @http.route(['/properties/<model("estate.property"):prop>'], type='http', auth="public", website=True)
    def property_detail(self, prop, **post):
        return request.render('estate.property_detail_template', {
            'property': prop,
        })

    @http.route(['/property/inquiry'], type='http', auth="public", website=True, methods=['GET', 'POST'], csrf=True)
    def property_inquiry(self, **post):
        if request.httprequest.method == 'GET':
            return request.render('estate.property_inquiry_form', {
                'properties': request.env['estate.property'].sudo().search([('state', 'in', ['new', 'offer_received'])]),
            })

        try:
            name = post.get('name')
            email = post.get('email')
            phone = post.get('phone')
            property_id = post.get('property_id')
            message = post.get('message')

            self._validate_inquiry_data(name, email)

            property_record = None
            if property_id:
                property_record = request.env['estate.property'].sudo().browse(int(property_id))
                if not property_record.exists():
                    property_record = None

            # Get the current user's partner if logged in, otherwise use the provided name
            partner_id = None
            if request.env.user != request.env.ref('base.public_user'):
                partner_id = request.env.user.partner_id.id
                # Use partner's name and email if not provided
                name = name or request.env.user.partner_id.name
                email = email or request.env.user.partner_id.email

            lead_data = {
                'name': f'Property Inquiry - {property_record.name if property_record else "General"}',
                'partner_name': name,
                'email_from': email,
                'phone': phone,
                'type': 'opportunity',  # Create opportunity instead of lead
                'partner_id': partner_id,
            }

            # Create description with Property Inquiry identifier for portal filtering
            description_parts = ['Property Inquiry']
            if property_record:
                description_parts.append(f"Inquiry for property: {property_record.name}")
                description_parts.append(f"Price: ${property_record.expected_price}")
            if message:
                description_parts.append(message)

            lead_data['description'] = '\n\n'.join(description_parts)

            lead = request.env['crm.lead'].sudo().create(lead_data)

            return request.render('estate.inquiry_success_template', {
                'lead': lead,
                'property': property_record,
                'success_message': 'Your inquiry has been submitted successfully!',
            })

        except ValidationError as e:
            return request.render('estate.inquiry_error_template', {
                'error_message': str(e),
            })
        except Exception:
            _logger.exception("Exception during property inquiry submission")
            return request.render('estate.inquiry_error_template', {
                'error_message': 'An unexpected error occurred',
            })


class EstateController(http.Controller):
    @http.route('/estate/get_property_data', type='json2', auth='public', website=True)
    def get_property_data(self, **kwargs):
        limit = int(kwargs.get('limit') or 3)
        sort = kwargs.get('sort') or 'name'
        category = kwargs.get('category') or 'all'
        show_price = kwargs.get('show_price') != 'false'

        # Build domain based on category
        domain = [('state', '=', 'new')]
        if category != 'all':
            # Find property type by name
            property_type = request.env['estate.property.type'].sudo().search([('name', '=', category)], limit=1)
            if property_type:
                domain.append(('property_type_id', '=', property_type.id))
            else:
                # If no property type found, return empty result
                return request.env['ir.ui.view']._render_template("estate.dynamic_filter_template_property_cards_estate", {
                    'records': [],
                    'show_price': show_price,
                })

        # Get properties
        properties = request.env['estate.property'].sudo().search(
            domain,
            limit=limit
        )

        # Apply sorting
        if sort == 'price':
            properties = properties.sorted('expected_price', reverse=True)
        else:
            properties = properties.sorted('name')

        return request.env['ir.ui.view']._render_template("estate.dynamic_filter_template_property_cards_estate", {
            'records': [{'_record': p} for p in properties],
            'show_price': show_price,
        })
