from odoo import http
from odoo.http import Controller, request, Response, route


class EstateController(Controller):
    @http.route('/properties',auth="public",website=True)   
    def all_views(self):
        properties = request.env['estate.property'].search([])
        return request.render('estate.properties_template', {'properties':properties})
    
    @http.route("/properties/<model('estate.property'):property>",type="http",auth="public",)
    def property_detail(self, property, **kwargs):
        return request.render("estate.property_detail_page", {"property": property})
