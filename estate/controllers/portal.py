from odoo import http
from odoo.http import request, route
from odoo.addons.portal.controllers.portal import pager as portal_pager


class PropertyPortal(http.Controller):

    @route(['/property', '/property/page/<int:page>'], auth='public', website=True, type="http")
    def show_properties(self, page=1, **kwargs):
        page_limit = 6
        total_properties = request.env['estate.property'].sudo().search_count([('state', 'in', ('new', 'offer accepted', 'offer received')), ('active', '=', True)])

        pager = portal_pager(
                url="/property",
                total=total_properties,
                page=page,
                step=page_limit
            )
        properties = request.env['estate.property'].sudo().search([('state', 'in', ('new', 'offer accepted', 'offer received')), ('active', '=', True)], limit=page_limit, offset=pager['offset'])
        return request.render('estate.estate_property_template', {
            'properties': properties,
            'pager': pager,
        })

    @route('/property/<int:property_id>', type='http', auth='public', website=True)
    def property_details(self, property_id, **kwargs):
        property_details = request.env['estate.property'].browse(property_id)
        return request.render('estate.estate_property_detail_template', {
            'property': property_details,
        })
