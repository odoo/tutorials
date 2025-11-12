from odoo import http
from odoo.http import request

from odoo.addons.portal.controllers.portal import pager as portal_pager 


class propertyWebsiteController(http.Controller):

    @http.route(['/properties', '/properties/page/<int:page>'], website=True, auth='public', type='http')
    def property_website(self, page=1, **kwargs):
        property_limit_per_page = 6
        property_count = request.env["estate.property"].sudo().search_count(
            domain=[('state','in',('new', 'offer received', 'offer accepted')), ('active', '=', True)]
        )
        pager = portal_pager(
            url="/properties",
            total=property_count,
            page=page,
            step=property_limit_per_page
        )
        property = request.env["estate.property"].sudo().search(
            domain=[('state','in',('new', 'offer received', 'offer accepted')), ('active', '=', True)],
            offset=pager['offset'],
            limit=property_limit_per_page
        )
        return request.render('estate.estate_property_website_template', 
        {
            'properties': property,
            'pager': pager
        })
    

    @http.route('/property/<int:property_id>', website=True, auth='public', type='http')
    def property_detail_view(self, property_id):
        property = request.env['estate.property'].sudo().browse(property_id)
        return request.render('estate.estate_property_detail_template',
        {
            'property' : property,
        })
