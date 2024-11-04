import logging
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager

from odoo import http


class PropertyController(http.Controller):

    @http.route(["/properties", "/properties/page/<int:page>"], auth="public", type="http", website=True)
    def properties_controller(self, page=1, per_page=6, *args, **kwargs):
        try:
            page = int(page)
            limit = 6
            offset = (page - 1) * limit
            
            properties = request.env['estate.property'].search([('state', '!=', 'sold'), ('state', '!=', 'canceled')], limit=limit, offset=offset)
            total_properties = request.env['estate.property'].search_count([('state', '!=', 'sold'), ('state', '!=', 'canceled')])
            pager = portal_pager('/properties', total_properties, page=page, step=limit)
            values = {
                "properties": properties,
                "pager": pager
            }
            return request.render("estate.property_controller", values)

        except Exception:
            logging.exception()

    @http.route("/property/<int:property_id>", auth="public", type="http", website=True)
    def property_card(self, property_id, *args, **kwargs):
        try:
            property_record = request.env['estate.property'].browse(property_id)
            if not property_record.exists() or property_record.state in ['sold', 'canceled']:
                return request.not_found()

            offers = property_record.offer_ids

            values = {
                "property": property_record,
                "offers": offers,
            }
            return request.render("estate.property_card", values)

        except Exception:
            logging.exception()
            return request.not_found()
