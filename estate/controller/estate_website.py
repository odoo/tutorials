from odoo import http
from odoo.http import request

class EstateWebsite(http.Controller):

    @http.route(['/properties'], type='http', auth="public", website=True, methods=['GET'])
    def list_properties(self):
        properties = request.env['estate.property'].sudo().search(
            [
                ('is_published', '=', True),
                ('state', '!=', 'accepted'),
                ('state', '!=', 'sold'),
            ],
            order='name asc'
        )
        return request.render(
            'estate.property_listing_template',
            {
                'properties': properties
            }
        )

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
        return request.render('estate.property_listing_home_page', {
            'Properties': Properties,
        })

    @http.route('/aboutus', type='http', auth='public', website=True, methods=['GET'], csrf=False)
    def render_about_us_page(self):
        Agents = request.env['res.users'].sudo().search([], limit=4)
        return request.render('estate.property_listing_about_us_page', {
            'Agents' : Agents,
        })

    @http.route('/create_offer', type='http', auth='public', website=True, methods=['POST'])
    def create_offer(self, **kwargs):
        if request.env.user.id == request.env.ref('base.public_user').id:
            return request.redirect('/web/signup')

        property_id = kwargs.get('property_id')
        offer_price = kwargs.get('offerPrice')
        validity_days = kwargs.get('validityDays')

        if (not property_id or not offer_price or not validity_days):
            return request.redirect('/error?message=not enough data')

        try:
            property_id = int(property_id)
            offer_price = float(offer_price)
            validity_days = int(validity_days)
        except Exception as e:
            return request.redirect('/error?message="Something went wrong!!')

        property = request.env['estate.property'].sudo().browse(property_id)
        if not property.exists():
            return request.redirect('/error?message="property does not exists"')

        request.env['estate.property.offers'].sudo().create({
            'property_id': property.id,
            'price': offer_price,
            'validity_days': validity_days,
            'partner_id': request.env.user.partner_id.id,
        })

        return request.redirect('/properties')
