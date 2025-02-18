from odoo import http
from odoo.http import request

import math


class EstateController(http.Controller):
    @http.route(
        ["/properties", "/properties/page/<int:page>"], type="http", auth="public"
    )
    def display_estate_property(self, page=1, **kwargs):
        search_domain = ["|", ("state", "=", "new"), ("state", "=", "offer_received")]
        listed_after = kwargs.get("listed_after")
        offset = (page - 1) * 6
        if listed_after:
            search_domain.append(("create_date", ">", listed_after))
        properties = request.env["estate.property"].search(
            search_domain,
            limit=6,
            offset=offset,
        )
        total_count = request.env["estate.property"].search_count(search_domain)
        total_pages = math.ceil(total_count / 6)
        values = {
            "properties": properties,
            "total_pages": total_pages,
            "page": page,
            "listed_after": listed_after or None,
        }
        return request.render("estate.estate_property_display", values)

    @http.route("/properties/property/<int:property_id>")
    def display_estate_property_details(self, property_id):
        property = request.env["estate.property"].browse(property_id)
        values = {"property": property}
        return request.render("estate.estate_property_details_display", values)
