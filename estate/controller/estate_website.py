import base64
from odoo import http
from odoo.http import request

class EstateWebsite(http.Controller):

    @http.route(['/properties'], type='http', auth="public", website=True, methods=['GET'])
    def list_properties(self):
        properties = request.env['estate.property'].sudo().search(
            [
                ('is_published', '=', True),
                ('state', '!=', 'accepted'),
                ('state', '!=', 'cancelled'),
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
            [('is_published', '=', True)], limit=3,
        )
        return request.render('estate.property_listing_home_page', {
            'Properties': Properties,
        })

    @http.route('/aboutus', type='http', auth='public', website=True, methods=['GET'])
    def render_about_us_page(self):
        Agents = request.env['res.users'].sudo().search([
            ('groups_id', 'in', [
                request.env.ref('estate.estate_group_manager').id,
                request.env.ref('estate.estate_group_user').id
            ])
        ], limit=4)
        return request.render('estate.property_listing_about_us_page', {
            'Agents' : Agents,
        })

    @http.route('/create_offer', type='http', auth='public', website=True, methods=['POST'])
    def create_offer(self, **kwargs):
        if request.env.user.id == request.env.ref('base.public_user').id:
            return request.redirect('/web/login')

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
            return request.redirect('/error?message="property not exists"')

        request.env['estate.property.offers'].sudo().create({
            'property_id': property.id,
            'price': offer_price,
            'validity_days': validity_days,
            'partner_id': request.env.user.partner_id.id,
        })

        return request.redirect('/properties')

    @http.route('/create_new_property', type='http', auth='public', website=True, methods=['GET'])
    def create_new_property(self, **kwargs):
        property_tags = request.env['estate.property.tag'].sudo().search([])
        property_types = request.env['estate.property.type'].sudo().search([])
        return request.render('estate.property_listing_create_new_property', {
            'property_types' : property_types,
            'property_tags' : property_tags,
        })

    @http.route('/create_property', type='http', auth='public', website=True, methods=['POST'])
    def create_property(self, **kwargs):
        image_file = request.httprequest.files.get('image')

        image_data = None
        if image_file:
            image_data = base64.b64encode(image_file.read())
            image_data = image_data.decode('utf-8')

        property_name = kwargs.get("name")
        property_tag_ids = kwargs.get("property_tag_ids")
        property_type_id = kwargs.get("property_type_ids")
        postcode = kwargs.get("postcode")
        availability_date = kwargs.get("date_availability")
        expected_price = kwargs.get("expected_price")
        property_description = kwargs.get("description")
        bedrooms = kwargs.get("bedrooms")
        living_area = kwargs.get("living_area")
        facades = kwargs.get("facades")
        garage = kwargs.get("garage") == "True"
        garden = kwargs.get("garden") == "True"
        garden_orientation = kwargs.get("garden_orientation")
        garden_area = kwargs.get("garden_area") if garden else 0
        is_published = kwargs.get("is_published") == 'on'

        try:
            expected_price = float(expected_price)
        except ValueError:
            return request.redirect('/error_page')

        new_property = request.env['estate.property'].create({
            'name': property_name,
            'active': True,
            'property_type_id': int(property_type_id),
            'property_tag_ids': int(property_tag_ids) if property_tag_ids else None,
            'user_id': request.env.user.id,
            'description': property_description,
            'postcode': postcode,
            'date_availability': availability_date,
            'expected_price': expected_price,
            'image': image_data,
            'bedrooms': int(bedrooms) if bedrooms else 0,
            'living_area': int(living_area) if living_area else 0,
            'facades': int(facades) if facades else 0,
            'garage': garage,
            'garden': garden,
            'garden_orientation' : garden_orientation,
            'garden_area': int(garden_area),
            'is_published': is_published,
        })

        if new_property.exists():
            return request.render('estate.property_success', {'property' : new_property})

        return  request.redirect('/error_page')

    @http.route('/my/properties', type='http', auth='public', website=True, methods=['GET'])
    def my_properties(self, **kwargs):
        my_properties = request.env['estate.property'].sudo().search(
            [('user_id', '=', request.env.user.id)]
        )
        my_offers = request.env['estate.property.offers'].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)]
        )
        return request.render("estate.property_my_property", {
            "properties" : my_properties,
            "offers": my_offers,
        })
