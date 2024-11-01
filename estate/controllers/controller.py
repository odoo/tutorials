from odoo import http
from odoo.http import request


class estateController(http.Controller):
    @http.route(['/estate/properties', '/estate/properties/page/<int:page>'], auth='public', website=True)
    def properties(self, page=1, **kwargs):
        domain = [('state', '!=', 'cancelled'), ('state', '!=', 'sold'), ('active', '=', True)]
        total_properties = request.env['estate.property'].sudo().search(domain)
        pager_obj = request.website.pager(url="/estate/properties", total=len(total_properties), page=page, step=6, scope=3)
        properties = request.env['estate.property'].sudo().search(domain, offset=pager_obj['offset'], limit=6)
        return request.render('estate.estate_property_template', {'properties': properties, 'pager': pager_obj})

    @http.route(['/estate/property/<int:id>'], auth='public', website=True)
    def property(self, id=1, **kwargs):
        property = request.env['estate.property'].sudo().browse(id)
        return request.render('estate.estate_single_property_template', {'property': property})
