from odoo import http
from odoo.http import request, route
from odoo.addons.portal.controllers.portal import pager as portal_pager


class PropertyPortal(http.Controller):
    @route(['/property', '/property/page/<int:page>'],auth='public', website=True)
    def show_properties(self,page=1,**kw):
        page_limit=6
        page=int(page)
        offset = (page - 1) * page_limit

        total_properties = request.env['estate.property'].sudo().search_count([('state','in',('new', 'offer accepted', 'offer received')),('active','=',True)])

        pager = portal_pager(
                url="/property",
                total=total_properties,
                page=page,
                step=page_limit
            )
        properties = request.env['estate.property'].sudo().search([('state','in',('new', 'offer accepted', 'offer received')),('active','=',True)], limit=page_limit, offset=offset)
        return request.render('estate.estate_property_template', {
            'properties': properties,
            'pager': pager,
        })