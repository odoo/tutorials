from odoo import http
from odoo.http import request


class PropertyController(http.Controller):

    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def properties(self, page=1, **kwargs):
        domain = ['&', ('state', '!=', 'sold'), ('state', '!=', 'canceled')]
        limit = 6
        offset = (page - 1) * limit
        properties = request.env['estate.property'].search(domain, limit=limit, offset=offset)
        total_properties = request.env['estate.property'].search_count(domain)

        pager = request.website.pager(
            url='/properties',
            total=total_properties,
            page=page,
            step=limit,
        )

        return request.render('estate.properties_template', {
            'properties': properties,
            'pager': pager
        })

    @http.route('/property/<model("estate.property"):property_obj>', type='http', auth='public', website=True)
    def property(self, property_obj, **kwargs):
        return request.render('estate.property_template', {
            'property': property_obj
        })
