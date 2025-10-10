from odoo import http
from odoo.http import request


class PropertyController(http.Controller):

    @http.route(['/properties', '/properties/page/<int:page>'], type="http", auth="public", website=True)
    def propertyHandler(self, page=1, **kwargs):
        property = request.env['estate.property'].sudo()

        properties_per_page = 6

        total_properties = property.search_count([
            ('status', 'in', ['new', 'offer_received']),
            ('active', '=', True)
        ])

        pager = request.website.pager(
            url="/properties",
            total=total_properties,
            page=page,
            step=properties_per_page
        )

        properties = property.search([
            ('status', 'in', ['new', 'offer_received']),
            ('active', '=', True)
        ], limit=properties_per_page, offset=(page - 1) * properties_per_page)

        return request.render('estate.website_properties_list', {
            'properties': properties,
            'pager': pager
        })

    @http.route('/properties/<int:property_id>', type="http", auth="public", website=True)
    def property_detail(self, property_id, **kwargs):
        property = request.env['estate.property'].sudo().browse(property_id)
        return request.render('estate.website_property_detail', {'property': property})
