from odoo import http
from odoo.http import request 

class EstatePropertyController(http.Controller):

    #Page that lists all properties 
    @http.route('/properties', auth='public', type='http', website=True)
    def list_properties(self):
        properties = request.env['estate.property'].sudo().search([])
        return request.render('estate.property_list_template',{
            'properties' : properties
        })
    
    #page for viewing property details
    @http.route('/properties:<id>', auth='public', type='http', website=True)
    def property_details(self):
        property = request.env['estate.property'].sudo().search([])
        if property:
            return request.render('estate.property_details_template',{
                'property' : property
            })
    
    