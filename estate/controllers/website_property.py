from odoo import http
from odoo.http import request


class EstateWebsite(http.Controller):
    _property_per_page = 6

    @http.route(
        ["/properties", "/properties/page/<int:page>"],
        type="http",
        auth="public",
        website=True,
    )
    def website_properties(self, page=1, search="", **kwargs):
        website = request.website
        domain = [("state", "in", ("new", "offer_received"))]
        if search:
            domain.append(("name", "ilike", search))
        found_properties = request.env["estate.property"].sudo().search(domain)
        total = len(found_properties)
        pager = website.pager(
            url=request.httprequest.path.partition("/page/")[0],
            total=total,
            page=page,
            step=self._property_per_page,
            url_args={"search": search},
        )
        offset = pager["offset"]
        properties_to_display = found_properties[
            offset : offset + self._property_per_page
        ]

        return request.render(
            "estate.website_properties",
            {"properties": properties_to_display, "pager": pager},
        )
