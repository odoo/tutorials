from odoo import http
import math

class MyController(http.Controller):
    @http.route(route='/reports', auth='public')
    def hellorUser(self):
        userProperty= http.request.env['estate.property'].sudo().search([])
        print(userProperty)
        return http.request.render("estate.estate_property_offer_template",{
            'docs': userProperty
        })
    
    @http.route(route='/properties', website=True, auth='user', methods=['GET'])
    def properties(self):
        params= http.request.get_http_params()
        print(params)
        page= int(params.get('page', 1))
        limit= int(params.get('limit',6))
        
        offset= (page-1)*limit
        
        domain= [
            ('state','not in', ('sold', 'cancelled', 'offer_accepted')),
            ('active','=',True)
        ]
        
        all_properties= http.request.env['estate.property'].search(domain,offset=offset, limit=limit)
        
        total= http.request.env['estate.property'].sudo().search_count(domain)
        
        return http.request.render("estate.estate_property_website_grid_view",{
            'all_properties': all_properties,
            'total_arr': list(range(math.ceil(total/limit))),
            'current_page': page
        })
        
    @http.route(route="/properties/<int:property_id>", website=True, auth="user", methods=["GET"])
    def property_details(self, property_id):
        property_id= int(property_id)
        
        domain= [
            ('id','=',property_id)
        ]
        
        property_details= http.request.env['estate.property'].search(domain=domain)
        return http.request.render("estate.estate_property_website_single_view", {
            'property_details': property_details
        })