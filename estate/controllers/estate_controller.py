from datetime import datetime
from odoo import http
from odoo.http import request

class EstatePropertyController(http.Controller):
    @http.route('/properties',auth="public",website=True)
    def my_site(self,page=1,**kwargs):
        listed_after= kwargs.get('listed_after')
        page=int(page)
        domain=[]
        domain.append(('status', 'in', ['new', 'offer_received']))
        if listed_after:
            listed_after_date = datetime.strptime(listed_after, '%Y-%m-%d').date()
            domain.append(('date_availability','&gt;', listed_after_date))


        properties = request.env['estate.property'].sudo().search(domain,order='date_availability desc',limit=6, offset=(page-1)*6)
        total_properties = request.env['estate.property'].sudo().search_count([('status', 'in', ['new', 'offer_received'])])
        total_pages= (total_properties//6) + (1 if total_properties%6 != 0 else 0)
        return request.render("estate.property_page",{
            'properties':properties,
            'page':page,
            'total_pages':total_pages,
        })
    
    @http.route('/properties/<int:property_id>', auth='public', website=True)
    def property_detail(self, property_id, **kwargs):
        # Fetch the property based on the ID
        property = request.env['estate.property'].sudo().browse(property_id)
        
        # Render the template with the property data
        return request.render('estate.property_detail_page', {
            'property': property
        })