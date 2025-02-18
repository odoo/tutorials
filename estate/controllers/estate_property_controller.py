from odoo import http
from odoo.http import request

class  EstatePropertyController(http.Controller):

    @http.route(['/properties'], type='http', auth='public', website=True)
    def estate_property(self, **kw):
        properties = request.env['estate.property'].search([('state','in',['new','offer_received'])],limit=6)
        return request.render('estate.properties_page',{
            'properties': properties, 
        })