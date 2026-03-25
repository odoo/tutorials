from odoo import http
from odoo.http import request


class EstatePropertyController(http.Controller):

    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def properties_list(self, page=1):
        Property = request.env['estate.property'].sudo()
        step = 6
        total = Property.search_count([])
        pager = request.website.pager(url='/properties', total=total, page=page, step=step)
        properties = Property.search([], offset=pager['offset'], limit=step, order='id desc')
        return request.render('estate.properties_listing', {
            'properties': properties,
            'pager': pager,
        })
