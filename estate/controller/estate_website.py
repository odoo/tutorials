from odoo import http
from odoo.http import request

class EstateWebsite(http.Controller):

    @http.route(['/properties'], type='http', auth="public", website=True, methods=['GET'])
    def list_properties(self):
        properties = request.env['estate.property'].sudo().search(
            [('is_published', '=', True), ('state', '!=', 'sold')],
            order='name asc'
        )
        return request.render('estate.property_listing_template', {'properties': properties})

    @http.route('/property/details/<int:property_id>', type='http', auth='public', website=True, methods=['GET'])
    def property_details(self, property_id):
        property_obj = request.env['estate.property'].sudo().browse(property_id)
        if not property_obj.exists():
            return request.not_found()
        return request.render(
            'estate.property_detail_template', 
            {
                'property': property_obj
            }
        )

    @http.route('/', type='http', auth='public', website=True, methods=['GET'])
    def render_homepage(self):
        Properties = request.env['estate.property'].sudo().search(
            [('is_published', '=', True)], limit=3
        )
        Agents = request.env['res.users'].sudo().search([], limit=4)
        return request.render('estate.property_listing_home_page', {
            'Properties': Properties,
            'Agents': Agents,
        })

    @http.route('/aboutus', type='http', auth='public', website=True, methods=['GET'], csrf=False)
    def render_about_us_page(self):
        return request.render('estate.property_listing_about_us_page', {})

    @http.route('/create_offer', type='http', auth='public', website=True, methods=['POST'])
    def create_offer(self, **kwargs):
        try:
            property_id = int(kwargs.get('property_id'))
            offer_price = float(kwargs.get('offer_price'))
            validity_days = int(kwargs.get('validity_days'))
            user_name = kwargs.get('user_name', '').strip()
            user_email = kwargs.get('user_email', '').strip()
            user_id = kwargs.get('user_id')

            if not property_id or not offer_price or not validity_days or not user_name or not user_email:
                return request.redirect('/error?message')

            user = request.env['res.partner'].sudo().search([('id', '=', int(user_id))], limit=1)
            if not user:
                user = request.env['res.partner'].sudo().create({
                    'name': user_name,
                    'email': user_email
                })

            property = request.env['estate.property'].sudo().browse(property_id)
            if not property.exists():
                request.redirect('/error?message')

            request.env['estate.property.offers'].sudo().create({
                'price': offer_price,
                'partner_id': user.id,
                'property_id': property.id,
                'validity_days': validity_days,
            })

            return request.redirect('/properties')
        except Exception as e:
            return request.redirect('/error?message')
