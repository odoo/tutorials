from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError


class PropertyController(http.Controller):
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
            return request.render('estate.inquiry_form_template', {
                'properties': request.env['estate.property'].sudo().search([('state', 'in', ['new', 'offer_received'])]),
            })

        try:
            name = post.get('name')
            email = post.get('email')
            phone = post.get('phone')
            property_id = post.get('property_id')
            message = post.get('message')

            if not all([name, email]):
                raise ValidationError("Name and email are required fields")

            if '@' not in email or '.' not in email:
                raise ValidationError("Please enter a valid email address")

            property_record = None
            if property_id:
                property_record = request.env['estate.property'].sudo().browse(int(property_id))
                if not property_record.exists():
                    property_record = None

            lead_data = {
                'name': f'Property Inquiry - {property_record.name if property_record else "General"}',
                'partner_name': name,
                'email_from': email,
                'phone': phone,
                'description': message or 'Property inquiry submitted',
                'type': 'lead',
            }

            if property_record:
                lead_data.update({
                    'property_id': property_record.id,
                    'description': f"Inquiry for property: {property_record.name}\n\nPrice: ${property_record.expected_price}\n\n{message or ''}",
                })

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
        except Exception as e:
            return request.render('estate.inquiry_error_template', {
                'error_message': 'An error occurred while processing your inquiry. Please try again.',
            })


class EstateController(http.Controller):
    @http.route('/estate/get_property_data', type='json', auth='public', website=True)
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

    @http.route('/estate/get_price', type='json', auth='public')
    def get_property_price(self, **kwargs):
        try:
            property_id = kwargs.get('property_id')

            if not property_id:
                return {
                    'success': False,
                    'error': 'Property ID is required',
                    'price': None,
                }

            property_record = request.env['estate.property'].sudo().browse(int(property_id))
            if not property_record.exists():
                return {
                    'success': False,
                    'error': 'Property not found',
                    'price': None,
                }

            return {
                'success': True,
                'property_id': property_record.id,
                'property_name': property_record.name,
                'expected_price': property_record.expected_price,
                'selling_price': property_record.selling_price if property_record.selling_price > 0 else None,
                'best_offer': property_record.best_price if property_record.best_price > 0 else None,
                'currency': 'USD',
                'state': property_record.state,
            }

        except ValueError:
            return {
                'success': False,
                'error': 'Invalid property ID format',
                'price': None,
            }
        except Exception as e:
            return {
                'success': False,
                'error': 'An error occurred while fetching property price',
                'price': None,
            }

    @http.route('/estate/check_availability', type='json', auth='public')
    def check_property_availability(self, **kwargs):
        try:
            property_id = kwargs.get('property_id')
 
            if not property_id:
                return {
                    'success': False,
                    'error': 'Property ID is required',
                    'available': False,
                }

            property_record = request.env['estate.property'].sudo().browse(int(property_id))
            if not property_record.exists():
                return {
                    'success': False,
                    'error': 'Property not found',
                    'available': False,
                }

            availability_status = {
                'success': True,
                'property_id': property_record.id,
                'property_name': property_record.name,
                'state': property_record.state,
                'available': False,
                'message': '',
            }

            if property_record.state == 'new':
                availability_status.update({
                    'available': True,
                    'message': 'Property is available for purchase',
                })
            elif property_record.state == 'offer_received':
                availability_status.update({
                    'available': True,
                    'message': 'Property has offers received but still available',
                })
            elif property_record.state == 'offer_accepted':
                availability_status.update({
                    'available': False,
                    'message': 'Offer has been accepted, property under contract',
                })
            elif property_record.state == 'sold':
                availability_status.update({
                    'available': False,
                    'message': 'Property has been sold',
                })
            elif property_record.state == 'cancelled':
                availability_status.update({
                    'available': False,
                    'message': 'Property listing has been cancelled',
                })
  
            availability_status.update({
                'expected_price': property_record.expected_price,
                'best_price': property_record.best_price if property_record.best_price > 0 else None,
                'date_availability': property_record.date_availability.strftime('%Y-%m-%d') if property_record.date_availability else None,
            })

            return availability_status

        except ValueError:
            return {
                'success': False,
                'error': 'Invalid property ID format',
                'available': False,
            }
        except Exception as e:
            return {
                'success': False,
                'error': 'An error occurred while checking property availability',
                'available': False,
            }

    @http.route('/test/api', type='http', auth="public", website=True)
    def test_api_page(self, **post):
        properties = request.env['estate.property'].sudo().search([('state', 'in', ['new', 'offer_received'])], limit=5)
        return request.render('estate.test_api_template', {
            'properties': properties,
        })
