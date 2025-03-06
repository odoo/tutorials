from odoo import http
from odoo.http import request
from odoo.addons.website.models.website import pager as website_pager
from odoo.addons.estate.controllers.estate_property_controller import EstatePropertyController

class EstatePropertyAuctionController(EstatePropertyController):
    
    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def list_properties(self, page=1, **kwargs):
        min_price = kwargs.get('min_price')
        max_price = kwargs.get('max_price')
        prop_type = kwargs.get('prop_type')
        date_filter = kwargs.get('date_filter')
        prop_sale_type = kwargs.get('prop_sale_type')
        

        domain = [('state', 'in', ['new', 'offer_received'])]
        
        if min_price:
            try:
                min_price = float(min_price) if min_price else None
                domain.append(('expected_price', '>=', min_price))
            except ValueError:
                min_price = None
                
        if max_price:
            try:
                max_price = float(max_price) if max_price else None
                domain.append(('expected_price', '<=', max_price))
            except ValueError:
                max_price = None
                
        if prop_type:
            try:
                prop_type = int(prop_type)
                domain.append(('property_type_id', '=', prop_type))
            except ValueError:
                prop_type = None  # Ignore invalid values
                
        if date_filter:
            try:
                date_obj = fields.Date.from_string(date_filter)
                domain.append(('create_date', '>=', date_obj))
            except ValueError:
                date_filter = None
                
        if prop_sale_type:
            try:
                domain.append(('sale_type', '=', prop_sale_type))
            except ValueError:
                prop_sale_type = None    
                
        properties_per_page = 6
        total_properties = request.env['estate.property'].sudo().search_count(domain)

        properties = request.env['estate.property'].sudo().search(
            domain, limit=properties_per_page, offset=(page - 1) * properties_per_page
        )

        filter_query = {key: val or '' for key, val in kwargs.items()}
        pager = request.website.pager(
            url='/properties',
            url_args=filter_query,
            total=total_properties,
            page=page,
            step=properties_per_page
        )

        return request.render('estate.property_list_template', {
            'properties': properties,
            'pager': pager,
            'min_price': min_price,
            'max_price': max_price,
            'prop_type': prop_type,
            'date_filter': date_filter,
            'prop_sale_type': prop_sale_type,
        })
        
        
    @http.route(['/property/<int:property_id>/add-offer'], type='http', auth='public', website=True)
    def add_offer(self, property_id=None, page=1, **kwargs):
        property = request.env['estate.property'].sudo().browse(property_id)
        user = request.env.user.name
        values = {
            "name": user,
            "property": property
        }
        return request.render('estate_auction.property_add_offer_template', values)
    
    
    @http.route(['/property/<int:property_id>/offer-submit'], type='http', auth='public', website=True, methods=['POST'])
    def offer_submit(self, property_id=None, **kwargs):
        property = request.env['estate.property'].sudo().browse(property_id)
        user_name = kwargs.get('name')
        offer_price = kwargs.get('price', 0.0)
        expected_price = property.expected_price
        message = ""
        if float(offer_price) < expected_price:
            message = f"Offer price must be greater than the expected price ({expected_price})"
        else:
            request.env['estate.property.offer'].sudo().create({
                'price': float(offer_price),
                'partner_id': request.env.user.partner_id.id,  # Correctly linking partner
                'property_id': property_id
            })
            message = "Congratulations, your offer has been successfully created!"
        value = {
            "message" : message,
            "property_id" : property_id
        }
        return request.render('estate_auction.add_offer_acknowledged_template', value)
    