from odoo import http
from odoo.http import request
import math
from datetime import datetime


class EstatePropertyController(http.Controller):
    @http.route(["/properties", "/properties/page/<int:page>"], type="http", auth="public", website=True)
    def properties(self, page=1, **kwargs):
        property = request.env["estate.property"]
        offset = (page - 1) * 6
        filter_date = kwargs.get("filter_date")
        search_property = kwargs.get("search_property")
        domain = ["|", ("state", "=", "new"), ("state", "=", "offer_received")]
        if filter_date:
            domain.append(("create_date", ">", filter_date))
        if search_property:
            domain.append(("name", "ilike", search_property))
        properties_count = property.search_count(domain)
        total_pages = math.ceil(properties_count / 6)

        properties = property.search(
            domain, limit=6, offset=offset, order="create_date DESC"
        )
        return request.render(
            "estate.estate_property_view_template",
            {"properties": properties, "page": int(page), "total_pages": total_pages},
        )

    @http.route("/properties/<int:property_id>", type="http", auth="public", website=True)
    def estate_property_detail(self, property_id):
        property = request.env["estate.property"].browse(property_id)
        if not property.exists():
            return "Property not found"
        return request.render(
            "estate.estate_property_detail_template", {"property": property}
        )
