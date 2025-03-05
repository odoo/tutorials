from odoo.http import request, route
from odoo.addons.estate.controllers.estate_website import EstateWebsite

class EstateWebsiteOverride(EstateWebsite):  # Inherit the original controller
    
    @route(['/estate/properties', '/estate/properties/page/<int:page>'], auth='public', website=True)
    def list_estate_properties(self, page=1, **kwargs):
        
        response = super().list_estate_properties(page, **kwargs)
        properties = response.qcontext.get('properties')
        
        if 'is_auction' in kwargs:
            if kwargs['is_auction'] == '1':  
                properties = properties.filtered(lambda p: p.is_auction)
            elif kwargs['is_auction'] == '0':  
                properties = properties.filtered(lambda p: not p.is_auction)
                
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
        )
        
        response.qcontext.update({
            'properties': _page_properties,
            'pager': pager,
        })
        
        return response
