from odoo import http
from odoo.http import request


class WebsitePropertiesController(http.Controller):

    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth="public", website=True)
    def get_properties(self, page=1):
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

        # Fetch the properties for the current page
        properties = request.env['estate.property'].sudo().search(domain, offset=pager['offset'], limit=per_page, order='expected_price asc')

        values = {
            'properties': properties,
            'pager': pager,
        }
        return request.render('estate.properties_template', values)

    @http.route(['/properties/details/<int:id>'], type='http', auth='public', website=True)
    def get_property(self, id):
        values = {
            'property': request.env['estate.property'].sudo().browse(id)
        }
        return request.render('estate.property_template', values)
