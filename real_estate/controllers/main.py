from odoo import http
from odoo.http import request
from odoo.tools.float_utils import float_compare

class PropertyLsitController(http.Controller):
    @http.route(['/property', '/property/page/<int:page>'], auth='user', type='http', website=True)
    def get_property_list(self, page=1, **kwargs):
        page_size = 4
        offset = (int(page) - 1 ) * page_size
        properties = request.env['real.estate.property'].search([('status', 'in', ('new', 'offer_received'))], limit=page_size, offset=offset)
        total_properties = request.env['real.estate.property'].search_count([('status', 'in', ('new', 'offer_received'))])

        pager = request.website.pager(
            url="/property",
            total=total_properties,
            page=page,
            step=page_size
        )

        properties_list = []
        for property in properties:
            properties_list.append({
                'id': property.id,
                'name': property.name,
                'image': property.image,
                'expected_price': property.expected_price,
                'type': property.property_type_id.name if property.property_type_id else '',
                'tags': property.tag_ids.mapped('name'),
            })

        return request.render('real_estate.property_list_template', {'properties': properties_list, 'pager': pager,})

    @http.route('/property/<int:property_id>', auth='user', type='http', website=True, methods=['GET'])
    def view_property(self, property_id, **kwargs):
        # Fetch the specific property by ID
        property = request.env['real.estate.property'].browse(property_id)

        STATUS = {
            'new': 'New Listing',
            'offer_received': 'Offer Received',
            'offer_accepted': 'Offer Accepted',
            'sold': 'Sold'
            }

        if property.exists():
            property_data = {
                'id': property.id,
                'name': property.name,
                'image': property.image,
                'description': property.description,
                'postcode': property.postcode,
                'date_availability': property.date_availability,
                'expected_price': property.expected_price,
                'bedrooms': property.bedrooms,
                'living_area': property.living_area,
                'facades': property.facades,
                'garage': property.garage,
                'garden':property.garden,
                'garden_area': property.garden_area,
                'garden_orientation': property.garden_orientation,
                'status': STATUS.get(property.status, 'Unknown'),
                'type': property.property_type_id.name if property.property_type_id else '',
                'tags': property.tag_ids.mapped('name'),
                'offers': [
                    {'partner': offer.partner_id.name, 'price': offer.price}
                    for offer in property.offer_ids
                    ] if property.offer_ids else '',
            }

            return request.render('real_estate.property_view_template', {'property': property_data})

        else:
            return request.not_found()

    @http.route('/offer/<int:property_id>', auth='user', type='http', website=True, methods=['GET'])
    def make_offer_property(self, property_id, **kwargs):
        property = request.env['real.estate.property'].browse(property_id)

        if property.exists():
            property_data = {
                'id': property.id,
                'name': property.name,
                'image': property.image,
                'best_offer': max(property.offer_ids.mapped('price')) if property.offer_ids else '0',
            }
            return request.render('real_estate.property_make_offer_template', {'property': property_data})
        else:
            return request.not_found()

    @http.route('/submit_offer', auth='user', type='http', website=True, methods=['POST'])
    def submit_offer_property(self, property_id, best_price, price, validity, **kwargs):
        if not property_id or not price or not validity:
            return request.redirect('/property')
        
        if float_compare(float(best_price), float(price), 2) == 1:
            return request.redirect('/offer/'+ str(property_id) +"?error=Offer must be higher than " + str(best_price))
        
        if float_compare(0.0, float(price), 2) != -1:
            return request.redirect('/offer/'+ str(property_id) +"?error=A property offer price must be strictly positive")
        
        if int(validity) < 0:
            return request.redirect('/offer/'+ str(property_id) +"?error=A property offer validity must be strictly positive")

        offer = request.env['real.estate.property.offer'].create({
            'price': float(price),
            'validity': int(validity),
            'property_id': int(property_id),
            'partner_id': request.env.user.partner_id.id,
        })

        if offer:
            return request.redirect('/property/'+ str(property_id) +"?offer_submitted=true")
        else:
            return request.redirect('/property/'+ str(property_id) +"?error=Server Error!!!")
