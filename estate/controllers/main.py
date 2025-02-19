from odoo import http
from odoo.http import Controller, request, Response, route


class EstateController(Controller):
    @http.route('/properties',auth="public",website=True)
    def all_views(self,**kwargs):
        min_price = kwargs.get('min_price')
        max_price = kwargs.get('max_price')
        min_price = float(min_price) if min_price else 0
        max_price = float(max_price) if max_price else float(99999999999)
        domain=[]
        domain.append(('expected_price', '>=', min_price))
        domain.append(('expected_price', '<=', max_price))
        properties = request.env['estate.property'].search(domain)
        return request.render('estate.properties_template', {'properties':properties})
    
    @http.route("/properties/<model('estate.property'):property>",type="http",auth="public",website=True)
    def property_detail(self, property, **kwargs):
        return request.render("estate.property_detail_page", {"property": property})
