import math
import logging
from odoo.http import Controller, request, route


class PropertyController(Controller):

    @route(
        ["/properties", "/properties/page/<int:page>"],
        auth="public",
        type="http",
        website=True,
    )
    def properties_controller(self, page=1, per_page=6, *args, **kwargs):
        try:
            property_recode = request.env["estate.property"]
            page = int(page)
            per_page = int(per_page)
            offset = (page - 1) * per_page
            limit = per_page
            domain = [("state", "in", ["offer_recived", "offer_accepted"])]
            properties = property_recode.search(
                domain,
                limit=limit,
                offset=offset,
            )
            total_property = properties.search_count(domain)
            total_pages = math.ceil(total_property / per_page)
            pager = {
                "url": "/properties/page/" + str(page),
                "total": total_property,
                "page": page,
                "total_page": total_pages,
                "step": per_page,
            }
            values = {"properties": properties, "pager": pager}
            return request.render("estate.estate_properties_web", values)
        except Exception:
            logging.exception()

    @route(
        "/properties/<int:property_id>",
        auth="public",
        type="http",
        website=True,
        methods=["GET"],
    )
    def property_controller(self, property_id, *args, **kwargs):
        try:
            property_recode = request.env["estate.property"].browse(property_id)
            return request.render(
                "estate.estate_property_web", ({"property": property_recode})
            )
        except Exception:
            logging.exception()
