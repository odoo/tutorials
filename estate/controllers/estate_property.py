from odoo import http
from odoo.http import request
from datetime import datetime

class EstatePropertyController(http.Controller):

    
    @http.route(['/properties', '/properties/page/<int:page>'] , type = 'http' , auth = 'public' , website = True)
    def property_list(self , page=1 , **kwargs):
        Property = request.env['estate.property']
        domain = [('state', 'in', ['new', 'offer_received'])]
        _url_arguments = {}

        if kwargs.get('listed_after'):
            domain += [('create_date' , '>=' , kwargs['listed_after'])]
            _url_arguments = {'listed_after' : kwargs['listed_after']}
            
        Property.sudo().search(
            domain , order = 'create_date desc'
        )

        properties_count = Property.search_count(domain)
        pager = request.website.pager(

            url='/properties',
            total=properties_count,
            page=page,
            step=6, 
            url_args=_url_arguments
        )

        properties = Property.search(domain, limit=6, offset=pager['offset'])
        return request.render('estate.property_listing', {
            'properties': properties,
            'pager': pager,
            'listed_after' : kwargs.get('listed_after' , False)
        })
    
    @http.route('/property/<model("estate.property"):estate_property>', type='http', auth='public', website=True)
    def property_detail(self, estate_property, **kwargs):
        return request.render('estate.property_detail', {
            'property': estate_property,
        })
