from datetime import datetime
import math

from odoo import http
from odoo.http import request, route


class EstatePropertyController(http.Controller):
    @http.route(
        ["/properties", "/properties/page/<int:page>"],
        type="http",
        auth="public",
        website=True,
        methods=["GET", "POST"],
    )
    def show_properties(self, page=1, listed_after=None, search=None, **post):
        domain = [("state", "in", ["new", "offer received"])]
        # current issue is that the list and search wont be stacked it will rather overwrite will add this feature soon.
        if search:
            domain = [
                "&",
                ("state", "in", ["new", "offer received"]),
                ("name", "ilike", search),
            ]
        if listed_after:
            try:
                date_filter = datetime.strptime(listed_after, "%Y-%m-%d")
                domain = [
                    "&",
                    ("state", "in", ["new", "offer received"]),
                    ("create_date", ">", date_filter),
                ]
            except ValueError:
                pass
        properties = (
            request.env["estate.property"]
            .sudo()
            .search(domain, limit=6, offset=(int(page) - 1) * 6)
        )
        total_properties = request.env["estate.property"].sudo().search_count(domain)

        total_pages = math.ceil(total_properties / 6)
        pager = request.website.pager(
            url="/properties",  # base URL
            total=total_properties,  # total item count
            page=page,  # current page
            step=6,  # items per page
            scope=total_pages,  # typically `self`
            url_args={},  # additional GET params if needed
        )
        return request.render(
            "estate.estate_property_webpage",
            {
                "properties": properties,
                "total_pages": int(total_pages),
                "current_page": int(page),
                "pager": pager,
            },
        )

    @http.route(
        "/properties/details/<model('estate.property'):property>",
        type="http",
        auth="public",
        website=True,
    )
    def property_details(self, property, **kw):
        return request.render("estate.estate_property_details", {"property": property})
