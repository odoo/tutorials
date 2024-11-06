from odoo import http
from odoo.http import request


class EstatePropertyWebsiteController(http.Controller):
    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth="public", website=True)
    def all_properties(self, page=0):
        domain = [('state', 'not in', ['sold', 'canceled'])]
        total_properties = request.env['estate.property'].sudo().search(domain)
        total_count = len(total_properties)
        per_page = 6
        pager = request.website.pager(
            url='/properties', 
            total=total_count, 
            page=page,
            step=per_page, 
            scope=3,
            url_args=None
        )

        properties = request.env['estate.property'].sudo().search(domain, offset=pager['offset'], limit=per_page)
        
        values = {
            'properties': properties,
            'pager': pager,
        }
        return request.render('estate.estate_property_website_template', values)

    @http.route(['/properties/details/<int:id>'], type='http', auth='public', website=True)
    def get_property(self, id):
        values = {
            'property': request.env['estate.property'].sudo().browse(id)
        }
        return request.render('estate.property_template', values)
