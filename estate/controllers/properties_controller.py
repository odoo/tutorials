from odoo import http
from odoo.http import request

class PropertiesController(http.Controller):
    # ------------------------------------------------------------
    # AVAILABLE PROPERTIES
    # ------------------------------------------------------------

    @http.route(['/properties','/properties/<int:page>'],
            type='http', auth="public", website=True)
    def properties(self,page=1,**kwargs):
        properties_per_page=6
        properties=request.env['estate.property'].search([('status','not in',['Sold','Cancelled']),('active','=','False')],limit=properties_per_page)
        total_properties=request.env['estate.property'].search_count([('status','not in',['Sold','Cancelled']),('active','=','False')])
        total_pages=(total_properties-1)//properties_per_page
        return request.render('estate.properties_template', {
            'properties': properties,
            'page': page,
            'total_pages': total_pages+1,
        })
    
    @http.route(['/property','/property/<int:property_id>'],type='http', auth="public", website=True)
    def get_property_details(self,property_id=None,**kwargs):
        property=request.env['estate.property'].sudo().browse(property_id)
        if not property.exists():
            return request.not_found()
        return request.render('estate.template_property_details',{"prop_details":property})