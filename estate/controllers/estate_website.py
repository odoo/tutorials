from odoo import http
from odoo.http import request


class EstateWebsite(http.Controller): 
    @http.route(['/estate/properties', '/estate/properties/page/<int:page>'], auth='public', website=True)
    def list_estate_properties(self, page=1, **kwargs):
        domain = [('state', 'in', ['new','offer_received'])]
        _url_arguments = {}
        
        # add extra domain if a date filter is provided
        if kwargs.get('listed_after'):
            domain += [('create_date', '>=', kwargs['listed_after'])]
            _url_arguments = {'listed_after' : kwargs['listed_after']}
        
        # Sort properties in descending order of creation
        properties = request.env['estate.property'].sudo().search(
            domain, order='create_date desc'
        )
        
        #paginate the properties
        _items_per_page = 6
        _total = len(properties)
        _starting_index = (page - 1) * _items_per_page
        _page_properties = properties[_starting_index: _starting_index + _items_per_page]
        
        pager = request.website.pager(
            url='/estate/properties',
            total=_total,
            page=page,
            step=_items_per_page,
            scope=4,
            url_args=_url_arguments
        )
        
        return request.render('estate.estate_website_properties', {
            'properties': _page_properties,
            'pager': pager,
            'listed_after' : kwargs.get('listed_after', False) # the 2nd parameter is the default value
        })
    
    @http.route(['/estate/property/<int:property_id>'], auth='public', website=True)
    def estate_property_detail(self, property_id):
        property_record = request.env['estate.property'].sudo().browse(property_id)
        
        if not property_record.exists():
            return request.render('website.page_404')
        
        return request.render('estate.estate_website_property_detail',{
            'property' : property_record
        })
