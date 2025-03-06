from odoo import fields, http
from odoo.http import request
from datetime import datetime
from odoo.addons.website.models.website import pager as website_pager

class EstatePropertyController(http.Controller):

    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def list_properties(self, page=1, **kwargs):
        min_price = kwargs.get('min_price')
        max_price = kwargs.get('max_price')
        prop_type = kwargs.get('prop_type')
        date_filter = kwargs.get('date_filter')

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

        # Pagination
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
        })

    @http.route('/property/<int:property_id>', type="http", auth="public", website=True)
    def property_details(self, property_id, **kwargs):
        property = request.env['estate.property'].sudo().browse(property_id)
        values = {
            "property": property
        }
        return request.render('estate.property_detail_template', values)