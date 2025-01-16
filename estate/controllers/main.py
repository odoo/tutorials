from odoo import http
from odoo.http import request

class list_properties_website(http.Controller):
    @http.route([
        '/properties',
        '/properties/page/<int:page>',
    ], type='http', auth="public", website=True, sitemap=True)
    
    def properties(self, page=1):
        items_per_page = 6
        Property = request.env['estate.property']
        total_properties = Property.search_count([  
            '&',('state','in',['new','offer_received','offer_accepted']),
            ('active','=',True)])
        
        properties = Property.search([
            '&',('state','in',['new','offer_received','offer_accepted']),
            ('active','=',True)
        ], limit=items_per_page, offset=(page - 1) * items_per_page)
        
        pager = request.website.pager(
            url="/properties",
            total=total_properties,
            page=page,
            step=items_per_page,
            scope=5)

        return request.render('estate.property_list_template', {
            'properties': properties,
            'pager': pager,
        })


    @http.route([
        '/properties/<model("estate.property"):property>',
    ], type='http', auth="public", website=True, sitemap=True)
    
    def property_details(self, property):
        
        return request.render('estate.property_details_template', {
            'property': property,
        })
