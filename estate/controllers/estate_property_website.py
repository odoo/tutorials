from odoo import http
from odoo.http import request


class Academy(http.Controller):
    @http.route(
        ["/properties", "/properties/page/<int:page>"],
        type="http",
        auth="public",
        website=True,
    )
    def index(self, page=1, **kw):
        step = 6
        offset = (page - 1) * step
        total_properties = (
            request.env["estate.property"]
            .sudo()
            .search_count(
                [
                    "&",
                    ("status", "in", ["new", "offer_received", "offer_accepted"]),
                    ("active", "=", True),
                ],
            )
        )
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
            url="/properties", total=total_properties, step=step, page=page
        )

        return request.render(
            "estate.website_list_template",
            {"properties": properties, "pager": pager},
        )

    @http.route(
        "/property/<model('estate.property'):property>",
        type="http",
        auth="public",
        website=True,
    )
    def property_detail(self, property, **kwargs):
        return request.render("estate.property_detail_page", {"property": property})
