from odoo import http
from odoo.http import request


class EstatePropertyController(http.Controller):
    @http.route(route=['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def list_properties(self, page=1, **kwargs):
        min_price = kwargs.get('min_price')
        max_price = kwargs.get('max_price')
        property_type = kwargs.get('property_type')

        domain = ['|', ('state', '=', 'new'), ('state', '=', 'offer_received')]  # Show only available properties

        if min_price:
            domain.append(('expected_price', '>=', float(min_price)))
        if max_price:
            domain.append(('expected_price', '<=', float(max_price)))
        if property_type:
            domain.append(('property_type_id.name', '=', property_type))

        properties_per_page = 3 
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
        
        return request.render('estate.website_property_listing_template', {
            'properties': properties,
            'pager': pager
        })

    @http.route(route='/property-details/<int:property_id>', type='http', auth="user", website=True)
    def property_details(self, property_id, **kwargs):
        # Fetch all property details from the estate.property model
        property = request.env['estate.property'].browse(property_id)
        return request.render('estate.wesite_property_details_template', {
            'property': property,
        })
