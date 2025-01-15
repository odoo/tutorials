from odoo import http
from odoo.http import request


class EstateWebsite(http.Controller):
    @http.route(
        ["/properties", "/properties/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def list_properties(self, page=1, **kwargs):
        step = 6
        offset = (page - 1) * step

        #! Fetch only the properties for the current page
        properties = (
            request.env["estate.property"]
            .sudo()
            .search(
                [
                    "&",
                    ("status", "in", ["new", "offer_received", "offer_accepted"]),
                    ("active", "=", True),
                ],
                limit=step,
                offset=offset,
            )
        )

        pager = request.website.pager(
            url="/properties", total=len(properties), step=step, page=page
        )

        # Render the template with paginated properties and the pager
        return request.render(
            "estate.listing_page",
            {"properties": properties, "pager": pager},
        )

    @http.route(
        "/property/<model('estate.property'):property>",
        type="http",
        auth="user",
        website=True,
    )
    def property_detail(self, property, **kwargs):
        return request.render("estate.property_detail_page", {"property": property})
