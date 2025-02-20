from odoo import http, fields
from odoo.http import request

class EstateProperty(http.Controller):

    @http.route(['/properties', '/properties/page/<int:page>'], auth='public', website=True)
    def list_estate_properties(self, page=1, **kwargs):
        domain = [('state', 'in', ['new','offer_received','offer_accepted'])]

        listed_after = kwargs.get('listed_after')
        if listed_after:
            try:
                filter_date = fields.Datetime.to_datetime(listed_after + " 00:00:00")
                domain.append(('create_date', '>=', filter_date))
            except ValueError:
                pass

        properties = request.env['estate.property'].sudo().search(domain, order="create_date desc")
        _items_per_page = 6
        _total = len(properties)
        _starting_index = (page - 1) * _items_per_page
        _page_properties = properties[_starting_index: _starting_index + _items_per_page]
        
        pager = request.website.pager(
            url='/properties',
            total=_total,
            page=page,
            step=_items_per_page,
            scope=4,
            url_args={'listed_after': listed_after} if listed_after else {}
        )
        
        return request.render('estate.estate_property_listing_template', {
            'properties': _page_properties,
            'pager': pager,
        })
    
    @http.route(['/property/<int:property_id>'], type='http', auth="public", website=True)
    def property_details(self, property_id, **kwargs):
        property_record = request.env['estate.property'].sudo().browse(property_id)
        if not property_record.exists():
            return request.render('website.404')

        return request.render('estate.estate_property_template', {'property': property_record})
