from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager

import math


class EstateController(http.Controller):
    @http.route(
        ["/properties", "/properties/page/<int:page>"],
        type="http",
        auth="public",
        website=True,
    )
    def display_estate_property(self, page=1, **kwargs):
        search_domain = ["|", ("state", "=", "new"), ("state", "=", "offer_received")]
        listed_after = kwargs.get("listed_after")
        search = kwargs.get("search")
        offset = (page - 1) * 6
        if listed_after:
            search_domain.append(("create_date", ">", listed_after))
        if search:
            search_domain.append(("name", "ilike", search))
        properties = request.env["estate.property"].search(
            search_domain, limit=6, offset=offset, order="create_date desc"
        )
        total_count = request.env["estate.property"].search_count(search_domain)

        pager = portal_pager(
            url="/properties",
            url_args={"search": search, "listed_after": listed_after},
            total=total_count,
            page=page,
            step=6,
        )
        params = {"listed_after": listed_after or None, "search": search or ""}
        values = {
            "properties": properties,
            "pager": pager,
            "page": page,
            "params": params,
        }
        return request.render("estate.estate_property_display", values)

    @http.route("/properties/property/<int:property_id>", auth="public", website=True)
    def display_estate_property_details(self, property_id):
        property = request.env["estate.property"].browse(property_id)
        values = {"property": property}
        return request.render("estate.estate_property_details_display", values)
